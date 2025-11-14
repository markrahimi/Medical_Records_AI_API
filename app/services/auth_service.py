from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from app.core.config import settings
from app.core.database import get_database
from app.services.email_service import email_service
from app.models.user import User, Token
from typing import Optional


class AuthService:
    def __init__(self):
        self.secret_key = settings.secret_key
        self.algorithm = settings.algorithm
        self.otp_storage = {}  # In-memory OTP storage (for production, use Redis)

    async def request_otp(self, email: str, name: str) -> bool:
        otp = email_service.generate_otp()
        expiry = datetime.now(timezone.utc) + timedelta(minutes=settings.otp_expire_minutes)
        self.otp_storage[email] = {
            "otp": otp,
            "name": name,
            "expiry": expiry
        }
        return await email_service.send_otp_email(email, otp)

    async def verify_otp(self, email: str, otp: str) -> Optional[Token]:
        if email not in self.otp_storage:
            return None

        stored_data = self.otp_storage[email]

        if stored_data["otp"] != otp:
            return None

        if datetime.now(timezone.utc) > stored_data["expiry"]:
            del self.otp_storage[email]
            return None

        db = get_database()
        user_data = await db.users.find_one({"email": email})

        if not user_data:
            user_doc = {
                "name": stored_data["name"],
                "email": email,
                "created_at": datetime.now(timezone.utc)
            }
            result = await db.users.insert_one(user_doc)
            user_id = str(result.inserted_id)
        else:
            user_id = str(user_data["_id"])

        del self.otp_storage[email]
        token = self.create_access_token({"sub": user_id, "email": email})
        return Token(access_token=token)

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    async def get_current_user(self, token: str) -> Optional[User]:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            user_id: str = payload.get("sub")
            email: str = payload.get("email")

            if user_id is None or email is None:
                return None

            db = get_database()
            user_data = await db.users.find_one({"email": email})

            if user_data is None:
                return None

            return User(
                id=str(user_data["_id"]),
                name=user_data["name"],
                email=user_data["email"],
                created_at=user_data["created_at"]
            )

        except JWTError:
            return None


auth_service = AuthService()
