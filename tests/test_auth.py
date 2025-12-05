from datetime import datetime, timedelta, timezone

import pytest
from jose import jwt
from jose.exceptions import JWTError

from app.core.config import settings
from app.services.auth_service import AuthService


class TestAuthService:
    def setup_method(self):
        self.auth_service = AuthService()

    def test_create_access_token(self):
        data = {"sub": "user123", "email": "test@example.com"}
        token = self.auth_service.create_access_token(data)

        assert token is not None
        assert isinstance(token, str)

        # Decode and verify token
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        assert payload["sub"] == "user123"
        assert payload["email"] == "test@example.com"
        assert "exp" in payload

    def test_token_contains_expiration(self):
        data = {"sub": "user123", "email": "test@example.com"}
        token = self.auth_service.create_access_token(data)

        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        exp_timestamp = payload["exp"]
        exp_datetime = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)

        # Token should expire in the future
        assert exp_datetime > datetime.now(timezone.utc)

    def test_token_expiration_time(self):
        data = {"sub": "user123", "email": "test@example.com"}
        token = self.auth_service.create_access_token(data)

        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        exp_timestamp = payload["exp"]
        exp_datetime = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)

        expected_expiry = datetime.now(timezone.utc) + timedelta(
            minutes=settings.access_token_expire_minutes
        )

        # Allow 1 minute tolerance
        time_diff = abs((exp_datetime - expected_expiry).total_seconds())
        assert time_diff < 60

    def test_otp_storage_initialization(self):
        assert self.auth_service.otp_storage == {}
        assert isinstance(self.auth_service.otp_storage, dict)

    def test_auth_service_has_required_attributes(self):
        assert hasattr(self.auth_service, "secret_key")
        assert hasattr(self.auth_service, "algorithm")
        assert hasattr(self.auth_service, "otp_storage")
        assert self.auth_service.secret_key == settings.secret_key
        assert self.auth_service.algorithm == settings.algorithm


class TestTokenValidation:
    def setup_method(self):
        self.auth_service = AuthService()

    def test_decode_valid_token(self):
        data = {"sub": "user123", "email": "test@example.com"}
        token = self.auth_service.create_access_token(data)

        # Token should be decodable
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        assert payload["sub"] == "user123"

    def test_decode_token_with_wrong_secret(self):
        data = {"sub": "user123", "email": "test@example.com"}
        token = self.auth_service.create_access_token(data)

        with pytest.raises(JWTError):
            jwt.decode(token, "wrong_secret", algorithms=[settings.algorithm])

    def test_token_with_additional_claims(self):
        data = {"sub": "user123", "email": "test@example.com", "role": "admin"}
        token = self.auth_service.create_access_token(data)

        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        assert payload["role"] == "admin"
