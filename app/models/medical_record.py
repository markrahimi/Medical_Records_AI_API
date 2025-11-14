from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class PatientData(BaseModel):
    patient_name: str
    age: int
    symptoms: str
    medical_history: Optional[str] = None
    additional_info: Optional[Dict[str, Any]] = None


class MedicalAnalysis(BaseModel):
    analysis: str
    recommendations: list[str]


class MedicalRecordCreate(BaseModel):
    patient_data: PatientData


class MedicalRecord(BaseModel):
    id: str
    patient_data: PatientData
    ai_analysis: MedicalAnalysis
    created_at: datetime
    user_id: Optional[str] = None

    class Config:
        from_attributes = True
