from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, Header, HTTPException

from app.core.database import get_database
from app.models.medical_record import MedicalAnalysis, MedicalRecord, PatientData
from app.services.ai_service import ai_service
from app.services.auth_service import auth_service

router = APIRouter(prefix="/records", tags=["Medical Records"])


async def get_current_user_from_token(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = authorization.split(" ")[1]
    user = await auth_service.get_current_user(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authentication token")
    return user


@router.post("/analyze")
async def analyze_patient(patient_data: PatientData) -> MedicalAnalysis:
    analysis = await ai_service.analyze_patient_data(patient_data)
    return analysis


@router.post("", response_model=MedicalRecord)
async def create_record(patient_data: PatientData, user=Depends(get_current_user_from_token)):
    db = get_database()

    analysis = await ai_service.analyze_patient_data(patient_data)

    record_doc = {
        "patient_data": patient_data.model_dump(),
        "ai_analysis": analysis.model_dump(),
        "created_at": datetime.now(timezone.utc),
        "user_id": user.id,
    }

    result = await db.medical_records.insert_one(record_doc)

    return MedicalRecord(
        id=str(result.inserted_id),
        patient_data=patient_data,
        ai_analysis=analysis,
        created_at=record_doc["created_at"],
        user_id=user.id,
    )


@router.get("", response_model=list[MedicalRecord])
async def get_all_records(user=Depends(get_current_user_from_token)):
    db = get_database()

    cursor = db.medical_records.find()
    records = []

    async for doc in cursor:
        records.append(
            MedicalRecord(
                id=str(doc["_id"]),
                patient_data=PatientData(**doc["patient_data"]),
                ai_analysis=MedicalAnalysis(**doc["ai_analysis"]),
                created_at=doc["created_at"],
                user_id=doc.get("user_id"),
            )
        )

    return records
