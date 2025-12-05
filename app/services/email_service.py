import random
import string

import resend

from app.core.config import settings


class EmailService:
    def __init__(self):
        resend.api_key = settings.resend_api_key
        self.from_email = settings.from_email
        self.from_name = settings.from_name

    def generate_otp(self, length: int = 6) -> str:
        return ''.join(random.choices(string.digits, k=length))

    async def send_otp_email(self, to_email: str, otp: str) -> bool:
        try:
            html = f"""
            <html>
                <body style="font-family: Arial, sans-serif;">
                    <h2>Medical Records API - OTP Verification</h2>
                    <p>Your One-Time Password (OTP) is:</p>
                    <h1 style="color: #4CAF50; letter-spacing: 5px;">{otp}</h1>
                    <p>This OTP will expire in {settings.otp_expire_minutes} minutes.</p>
                    <p><strong>Do not share this code with anyone.</strong></p>
                    <hr>
                    <p style="color: #666; font-size: 12px;">
                        If you did not request this code, please ignore this email.
                    </p>
                </body>
            </html>
            """

            params = {
                "from": f"{self.from_name} <{self.from_email}>",
                "to": [to_email],
                "subject": "Your OTP Code - Medical Records API",
                "html": html,
            }

            resend.Emails.send(params)
            return True

        except Exception:
            return False


email_service = EmailService()
