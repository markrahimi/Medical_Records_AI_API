from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App settings
    app_name: str = "Medical Records AI API"
    version: str = "0.1.0"

    # MongoDB settings
    mongodb_url: str
    mongodb_db_name: str = "medical_records"

    # Groq AI settings
    groq_api_key: str
    groq_model: str = "llama-3.1-8b-instant"

    # Resend Email settings
    resend_api_key: str
    from_email: str = "onboarding@resend.dev"
    from_name: str = "Medical Records API"

    # JWT settings
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # OTP settings
    otp_expire_minutes: int = 10

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
