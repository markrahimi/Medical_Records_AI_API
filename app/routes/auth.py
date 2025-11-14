from fastapi import APIRouter, HTTPException
from app.models.user import UserCreate, OTPVerify, Token
from app.services.auth_service import auth_service

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/request-otp")
async def request_otp(user: UserCreate):
    success = await auth_service.request_otp(user.email, user.name)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to send OTP email")
    return {"message": f"OTP sent to {user.email}"}


@router.post("/verify-otp", response_model=Token)
async def verify_otp(otp_data: OTPVerify):
    token = await auth_service.verify_otp(otp_data.email, otp_data.otp)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid or expired OTP")
    return token
