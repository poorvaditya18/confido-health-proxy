from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from models.model import Appointment, Patient, Provider, Location

class IngestionRepository:
    def __init__(self, db: Session):
        self.db = db

    def upsert_patients(self, patients: dict):
        try:  
            for ehr_id, patient in patients.items():
                stmt = insert(Patient).values(
                    ehr_id=ehr_id,
                    given_name=patient.get("given_name"),
                    family_name=patient.get("family_name"),
                    phone=patient.get("phone")
                ).on_conflict_do_update(
                    index_elements=["ehr_id"],
                    set_={
                        "given_name": patient.get("given_name"),
                        "family_name": patient.get("family_name"),
                        "phone": patient.get("phone")
                    }
                )
                self.db.execute(stmt)
        except Exception as e:
            raise Exception(f"error upserting patients: {str(e)}")
    
    def upsert_providers(self, providers: dict):
        try: 
            for ehr_id, display_name in providers.items():
                stmt = insert(Provider).values(
                    ehr_id=ehr_id,
                    display_name=display_name
                ).on_conflict_do_update(
                    index_elements=["ehr_id"],
                    set_={"display_name": display_name}
                )
                self.db.execute(stmt)
        except Exception as e:
            raise Exception(f"error upserting provider: {str(e)}")
    
    def upsert_locations(self, locations: dict):
        try: 
            for ehr_id, display_name in locations.items():
                stmt = insert(Location).values(
                    ehr_id=ehr_id,
                    display_name=display_name
                ).on_conflict_do_update(
                    index_elements=["ehr_id"],
                    set_={"display_name": display_name}
                )
                self.db.execute(stmt)
        except Exception as e:
            raise Exception(f"error upserting locations: {str(e)}")
        
    def upsert_appointments(self, appointments: dict):
        try:
            for patient_ehr_id, appointments in appointments.items():
                for appt in appointments:
                    stmt = insert(Appointment).values(
                        ehr_id=appt.get("appointment_ehr_id"),
                        patient_ehr_id=appt.get("patient_ehr_id"),
                        provider_ehr_id=appt.get("provider_ehr_id"),
                        location_ehr_id=appt.get("location_ehr_id"),
                        start_time=appt.get("start_time")
                    ).on_conflict_do_update(
                        index_elements=["ehr_id"],
                        set_={
                            "patient_ehr_id": appt.get("patient_ehr_id"),
                            "provider_ehr_id": appt.get("provider_ehr_id"),
                            "location_ehr_id": appt.get("location_ehr_id"),
                            "start_time": appt.get("start_time")
                        }
                    )
                    self.db.execute(stmt)
        except Exception as e:
            raise Exception(f"error upserting appointments: {str(e)}")
