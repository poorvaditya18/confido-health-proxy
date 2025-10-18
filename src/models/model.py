from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from configs.db_config import Base

class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    ehr_id = Column(String, unique=True)
    given_name = Column(String)
    family_name = Column(String)
    phone = Column(String)

class Provider(Base):
    __tablename__ = "providers"
    id = Column(Integer, primary_key=True, index=True)
    ehr_id = Column(String, unique=True)
    display_name = Column(String)

class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True, index=True)
    ehr_id = Column(String, unique=True)
    display_name = Column(String)

class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, index=True)
    ehr_id = Column(String, unique=True)
    patient_ehr_id = Column(String, ForeignKey("patients.ehr_id"))
    provider_ehr_id = Column(String, ForeignKey("providers.ehr_id"))
    location_ehr_id = Column(String, ForeignKey("locations.ehr_id"))
    start_time = Column(DateTime)

    patient = relationship("Patient", foreign_keys=[patient_ehr_id])
    provider = relationship("Provider", foreign_keys=[provider_ehr_id])
    location = relationship("Location", foreign_keys=[location_ehr_id])