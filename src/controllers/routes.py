from fastapi import APIRouter, Depends, HTTPException, Query, Header
from sqlalchemy.orm import Session
from typing import List
from schemas.schemas import AppointmentSchema, PatientSchema
from services.appointment_service import AppointmentService
from services.patient_service import PatientService
from services.ingestion_service import IngestionService
from configs.db_singleton import get_db

router = APIRouter()

@router.post("/api/v1/ingest", tags=["ingest"])
async def ingest(x_source_type: str = Header(...), db: Session = Depends(get_db)):
    try:
        ingestion_service = IngestionService(db)
        response = ingestion_service.start_ingestion(source_type=x_source_type)
        return { "data": response }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except NotImplementedError as e:
        raise HTTPException(status_code=501, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))

@router.get("/api/v1/patients", response_model=List[PatientSchema])
async def get_patients(
    skip: int = 0, 
    limit: int = Query(10, le=50), 
    db: Session = Depends(get_db)):
    try:
        patient_service = PatientService(db)
        response = patient_service.get_all_patients(skip=skip, limit=limit)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/v1/appointments", response_model=List[AppointmentSchema])
def get_appointments(
    skip: int = 0, 
    limit: int = Query(10, le=50), 
    db: Session = Depends(get_db)
    ):
    try:
        appointment_service = AppointmentService(db)
        response = appointment_service.get_all_appointments(skip=skip, limit=limit)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))