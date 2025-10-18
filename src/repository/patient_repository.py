from sqlalchemy.orm import Session
from models.model import Patient

class PatientRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_patients(self, skip: int = 0, limit: int = 10):
        try: 
            response = self.db.query(Patient).offset(skip).limit(limit).all()
            return response
        except Exception as e:
            raise Exception(f"failed to fetch patients from database. err: {e}")