import logging
from sqlalchemy.orm import Session
from services.source_factory import SourceFactory
from repository.patient_repository import PatientRepository
logger = logging.getLogger("patient_service")

class PatientService:
    def __init__(self, db: Session):
        self.db = db
        self.patient_repository = PatientRepository(db)

    def get_all_patients(self, skip: int = 0, limit: int = 10):
        try: 
            response = self.patient_repository.get_patients(skip=skip, limit=limit)
            return response
        except Exception as e:
            raise Exception(f"failed to get all patients. err: {e}")
        
    def fetch_patients(self, source_type: str, patient_id: str):
        try:
            source_service = SourceFactory.get_source_service(source_type)
            patient_data = source_service.get_patient_data(patient_id)
            return patient_data
        except Exception as e:
            raise Exception(f"failed to fetch patient data for patient_id {patient_id}. err: {e}")