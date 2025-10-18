from sqlalchemy.orm import Session
from models.model import Appointment, Patient, Provider, Location

class AppointmentRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_appointments(self, skip: int = 0, limit: int = 10):
        try:
            return (
                self.db.query(
                    Appointment,
                    Patient.given_name,
                    Patient.family_name,
                    Patient.phone,
                    Provider.display_name.label("provider_name"),
                    Location.display_name.label("location_name")
                )
                .join(Patient, Appointment.patient_ehr_id == Patient.ehr_id)
                .join(Provider, Appointment.provider_ehr_id == Provider.ehr_id)
                .join(Location, Appointment.location_ehr_id == Location.ehr_id)
                .offset(skip)
                .limit(limit)
                .all()
            )
        except Exception as e:
            raise Exception(f"failed to fetch appointments from database. err: {e}")