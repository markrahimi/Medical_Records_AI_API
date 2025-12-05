"""
Authentication Service Module.

This module handles user authentication using OTP (One-Time Password)
verification via email and JWT token generation.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt

from app.core.config import settings
from app.core.database import get_database
from app.core.logging import logger
from app.models.user import Token, User
from app.services.email_service import email_service


class AuthService:
    """
    Service class for user authentication.

    Handles OTP generation, verification, and JWT token management.

    Attributes:
        secret_key: Secret key for JWT encoding.
        algorithm: Algorithm used for JWT encoding.
        otp_storage: In-memory storage for OTP codes.
    """

    def __init__(self):
        """Initialize the authentication service."""
        self.secret_key = settings.secret_key
        self.algorithm = settings.algorithm
        self.otp_storage = {}  # In-memory OTP storage (for production, use Redis)

    async def request_otp(self, email: str, name: str) -> bool:
        """
        Generate and send OTP to user's email.

        Args:
            email: User's email address.
            name: User's name.

        Returns:
            bool: True if OTP was sent successfully.
        """
        logger.debug(f"Generating OTP for user: {email}")
        otp = email_service.generate_otp()
        expiry = datetime.now(timezone.utc) + timedelta(minutes=settings.otp_expire_minutes)
        self.otp_storage[email] = {"otp": otp, "name": name, "expiry": expiry}
        logger.info(f"OTP requested for email: {email}")
        return await email_service.send_otp_email(email, otp)

    async def verify_otp(self, email: str, otp: str) -> Optional[Token]:
        """
        Verify OTP and generate JWT token.

        Args:
            email: User's email address.
            otp: One-time password to verify.

        Returns:
            Token: JWT access token if verification succeeds, None otherwise.
        """
        logger.debug(f"Verifying OTP for email: {email}")

        if email not in self.otp_storage:
            logger.warning(f"OTP verification failed: No OTP found for email {email}")
            return None

        stored_data = self.otp_storage[email]

        if stored_data["otp"] != otp:
            logger.warning(f"OTP verification failed: Invalid OTP for email {email}")
            return None

        if datetime.now(timezone.utc) > stored_data["expiry"]:
            del self.otp_storage[email]
            logger.warning(f"OTP verification failed: OTP expired for email {email}")
            return None

        db = get_database()
        user_data = await db.users.find_one({"email": email})

        if not user_data:
            user_doc = {
                "name": stored_data["name"],
                "email": email,
                "created_at": datetime.now(timezone.utc),
            }
            result = await db.users.insert_one(user_doc)
            user_id = str(result.inserted_id)
            logger.info(f"New user created: {email} with ID {user_id}")
        else:
            user_id = str(user_data["_id"])
            logger.info(f"Existing user logged in: {email}")

        del self.otp_storage[email]
        token = self.create_access_token({"sub": user_id, "email": email})
        logger.info(f"Access token generated for user: {email}")
        return Token(access_token=token)

    def create_access_token(self, data: dict) -> str:
        """
        Create a JWT access token.

        Args:
            data: Payload data to encode in the token.

        Returns:
            str: Encoded JWT token.
        """
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.access_token_expire_minutes
        )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    async def get_current_user(self, token: str) -> Optional[User]:
        """
        Get current user from JWT token.

        Args:
            token: JWT access token.

        Returns:
            User: User object if token is valid, None otherwise.
        """
        logger.debug("Validating access token")
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            user_id: str = payload.get("sub")
            email: str = payload.get("email")

            if user_id is None or email is None:
                logger.warning("Token validation failed: Missing user_id or email in payload")
                return None

            db = get_database()
            user_data = await db.users.find_one({"email": email})

            if user_data is None:
                logger.warning(f"Token validation failed: User not found for email {email}")
                return None

            logger.debug(f"Token validated successfully for user: {email}")
            return User(
                id=str(user_data["_id"]),
                name=user_data["name"],
                email=user_data["email"],
                created_at=user_data["created_at"],
            )

        except JWTError as e:
            logger.error(f"JWT decode error: {e}")
            return None


auth_service = AuthService()
