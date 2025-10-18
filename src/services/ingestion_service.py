import logging
from sqlalchemy.orm import Session
from repository.ingestion_repository import IngestionRepository
from services.patient_service import PatientService
from services.appointment_service import AppointmentService
logger = logging.getLogger("ingestion_service")

class IngestionService:
    def __init__(self, db:Session):
        self.db = db
        self.patient_list_ids = ["erXuFYUfucBZaryVksYEcMg3", "eq081-VQEgP8drUUqCWzHfw3", "eAB3mDIBBcyUKviyzrxsnAw3", "egqBHVfQlt4Bw3XGXoxVxHg3", "eIXesllypH3M9tAA5WdJftQ3"]
        self.patient_service = PatientService(db)
        self.appointment_service = AppointmentService(db)
        self.ingestion_repository = IngestionRepository(db)
    
    def fetch_data(self, source_type: str):
        try:
            patient_data_dict = {}
            appointment_data_dict = {}
            for patient_id in self.patient_list_ids:
                patient_data = self.patient_service.fetch_patients(source_type, patient_id)
                patient_data_dict[patient_id] = patient_data
                appointment_data = self.appointment_service.fetch_appointments(source_type, patient_id)
                appointment_data_dict[patient_id] = appointment_data
            
            filtered_patient_data = self.filter_patient_data(patient_data_dict)
            provider_data, location_data = self.resolve_provider_and_location_references(appointment_data_dict)
            filtered_appointment_data = self.filter_appointment_data(appointment_data_dict)

            return {
                "patients": filtered_patient_data,
                "providers": provider_data,
                "locations": location_data,
                "appointments": filtered_appointment_data,
            }
        except Exception as e:
            raise Exception(f"Error fetching data: {str(e)}")

    def filter_patient_data(self, patient_data_dict):
        filtered_patient_data = {}
        for patient_id, patient in patient_data_dict.items():
            given_name = None
            family_name = None
            phone = None

            if "name" in patient and isinstance(patient["name"], list) and len(patient["name"]) > 0:
                name_obj = patient["name"][0]
                given_name = " ".join(name_obj.get("given", [])) if "given" in name_obj else None
                family_name = name_obj.get("family")

            if "telecom" in patient and isinstance(patient["telecom"], list):
                for t in patient["telecom"]:
                    if t.get("system") == "phone":
                        phone = t.get("value")
                        break
            
            filtered_patient_data[patient_id] = {
                "given_name": given_name,
                "family_name": family_name,
                "phone": phone
            }
        return filtered_patient_data

    def resolve_provider_and_location_references(self, appointment_data_dict):
        location_map = {}
        provider_map = {}
        for patient_id, bundle in appointment_data_dict.items():
            if "entry" not in bundle:
                continue
            for entry in bundle["entry"]:
                resource = entry.get("resource", {})
                participants = resource.get("participant", [])
                for participant in participants:
                    actor = participant.get("actor", {})
                    ref = actor.get("reference")
                    display = actor.get("display")
                    if ref and ref.startswith("Practitioner/"):
                        provider_id = ref.split("/")[1]
                        if provider_id not in provider_map:
                            provider_map[provider_id] = display
                    if ref and ref.startswith("Location/"):
                        location_id = ref.split("/")[1]
                        if location_id not in location_map:
                            location_map[location_id] = display     
        return provider_map, location_map
    
    def filter_appointment_data(self, appointment_data_dict):
        filtered_appointment_data = {}
        for patient_id, bundle in appointment_data_dict.items():
            if "entry" not in bundle:
                continue

            patient_appointments = []
            for entry in bundle["entry"]:
                resource = entry.get("resource", {})
                appointment_id = resource.get("id")
                start_time = resource.get("start")
                provider_id = None
                location_id = None

                participants = resource.get("participant", [])
                for participant in participants:
                    actor = participant.get("actor", {})
                    ref = actor.get("reference")
                    if  ref and ref.startswith("Practitioner/"):
                        provider_id = ref.split("/")[1]
                    if  ref and ref.startswith("Location/"):
                        location_id = ref.split("/")[1]

                patient_appointments.append({
                    "appointment_ehr_id": appointment_id,
                    "patient_ehr_id": patient_id,
                    "provider_ehr_id": provider_id,
                    "location_ehr_id": location_id,
                    "start_time": start_time
                })

            filtered_appointment_data[patient_id] = patient_appointments

        return filtered_appointment_data

    def start_ingestion(self, source_type: str):
        counts = {
            "patients": 0,
            "providers": 0,
            "locations": 0,
            "appointments": 0
        }
        try:
            data = self.fetch_data(source_type)
            self.ingestion_repository.upsert_providers(data["providers"])
            counts["providers"] = len(data["providers"])

            self.ingestion_repository.upsert_locations(data["locations"])
            counts["locations"] = len(data["locations"])

            self.ingestion_repository.upsert_patients(data["patients"])
            counts["patients"] = len(data["patients"])
            
            self.ingestion_repository.upsert_appointments(data["appointments"])
            total_appointments = sum(len(appts) for appts in data["appointments"].values())
            counts["appointments"] = total_appointments
            self.ingestion_repository.db.commit()
        except Exception as e:
            self.ingestion_repository.db.rollback()
            raise Exception(f"ingestion failed for source : {source_type}. err: {str(e)}")

        return counts