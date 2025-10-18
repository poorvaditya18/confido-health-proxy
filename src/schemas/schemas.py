from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class PatientSchema(BaseModel):
    ehr_id: str
    given_name: str
    family_name: str
    phone: Optional[str] = None

    class Config:
        orm_mode = True

class AppointmentSchema(BaseModel):
    ehr_id: str
    start_time: datetime
    patient_name: str
    patient_phone: str
    provider_name: str
    location_name: str

    class Config:
        orm_mode = True