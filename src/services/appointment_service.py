from sqlalchemy.orm import Session
from services.source_factory import SourceFactory
from repository.appointment_repository import AppointmentRepository
from schemas.schemas import AppointmentSchema
import logging
logger = logging.getLogger("appointment_service")

class AppointmentService:
    def __init__(self, db: Session):
        self.db = db
        self.appointment_repository = AppointmentRepository(db)

    def get_all_appointments(self, skip: int = 0, limit: int = 10):
        try:
            raw_appointments = self.appointment_repository.get_appointments(skip=skip, limit=limit)
            results = []
            for a, given_name, family_name, phone, provider_name, location_name in raw_appointments:
                results.append(
                    AppointmentSchema(
                        ehr_id=a.ehr_id,
                        start_time=a.start_time,
                        patient_name=f"{given_name} {family_name}",
                        patient_phone=phone,
                        provider_name=provider_name,
                        location_name=location_name
                    )
                )
            return results
        except Exception as e:
            raise Exception(f"failed to get all appointments. err: {e}")
    
    def fetch_appointments(self, source_type: str, patient_id: str):
        try:
            source_service = SourceFactory.get_source_service(source_type)
            appointment_data = source_service.get_appointment_data(patient_id)
            return appointment_data
        except Exception as e:
            raise Exception(f"failed to fetch appointments for patient_id {patient_id}. err: {e}")