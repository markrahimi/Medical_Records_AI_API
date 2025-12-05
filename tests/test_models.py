from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from app.models.medical_record import MedicalAnalysis, MedicalRecord, PatientData
from app.models.user import OTPVerify, Token, User, UserCreate


class TestPatientData:
    def test_create_patient_data_with_required_fields(self):
        patient = PatientData(
            patient_name="John Doe",
            age=30,
            symptoms="headache, fever",
        )
        assert patient.patient_name == "John Doe"
        assert patient.age == 30
        assert patient.symptoms == "headache, fever"
        assert patient.medical_history is None
        assert patient.additional_info is None

    def test_create_patient_data_with_all_fields(self):
        patient = PatientData(
            patient_name="Jane Doe",
            age=25,
            symptoms="cough, sore throat",
            medical_history="Asthma",
            additional_info={"allergies": ["penicillin"]},
        )
        assert patient.patient_name == "Jane Doe"
        assert patient.medical_history == "Asthma"
        assert patient.additional_info == {"allergies": ["penicillin"]}

    def test_patient_data_missing_required_field(self):
        with pytest.raises(ValidationError):
            PatientData(patient_name="John", age=30)  # missing symptoms

    def test_patient_data_invalid_age_type(self):
        with pytest.raises(ValidationError):
            PatientData(patient_name="John", age="thirty", symptoms="headache")

    def test_patient_data_negative_age(self):
        # Pydantic allows negative integers by default
        patient = PatientData(patient_name="Test", age=0, symptoms="test")
        assert patient.age == 0


class TestMedicalAnalysis:
    def test_create_medical_analysis(self):
        analysis = MedicalAnalysis(
            analysis="Patient shows symptoms of common cold.",
            recommendations=["Rest", "Drink fluids", "Take vitamin C"],
        )
        assert "common cold" in analysis.analysis
        assert len(analysis.recommendations) == 3

    def test_medical_analysis_empty_recommendations(self):
        analysis = MedicalAnalysis(
            analysis="No significant findings.",
            recommendations=[],
        )
        assert analysis.recommendations == []

    def test_medical_analysis_missing_field(self):
        with pytest.raises(ValidationError):
            MedicalAnalysis(analysis="Test")  # missing recommendations


class TestMedicalRecord:
    def test_create_medical_record(self):
        patient = PatientData(patient_name="John", age=30, symptoms="fever")
        analysis = MedicalAnalysis(analysis="Test", recommendations=["Rest"])
        record = MedicalRecord(
            id="123",
            patient_data=patient,
            ai_analysis=analysis,
            created_at=datetime.now(timezone.utc),
            user_id="user123",
        )
        assert record.id == "123"
        assert record.patient_data.patient_name == "John"
        assert record.user_id == "user123"

    def test_medical_record_without_user_id(self):
        patient = PatientData(patient_name="John", age=30, symptoms="fever")
        analysis = MedicalAnalysis(analysis="Test", recommendations=["Rest"])
        record = MedicalRecord(
            id="123",
            patient_data=patient,
            ai_analysis=analysis,
            created_at=datetime.now(timezone.utc),
        )
        assert record.user_id is None


class TestUserModels:
    def test_create_user(self):
        """Test creating a user."""
        user = User(
            id="user123",
            name="John Doe",
            email="john@example.com",
            created_at=datetime.now(timezone.utc),
        )
        assert user.id == "user123"
        assert user.name == "John Doe"
        assert user.email == "john@example.com"

    def test_user_create_model(self):
        user_create = UserCreate(name="Jane", email="jane@example.com")
        assert user_create.name == "Jane"
        assert user_create.email == "jane@example.com"

    def test_user_create_invalid_email(self):
        with pytest.raises(ValidationError):
            UserCreate(name="John", email="invalid-email")

    def test_otp_verify_model(self):
        otp = OTPVerify(email="test@example.com", otp="123456")
        assert otp.email == "test@example.com"
        assert otp.otp == "123456"

    def test_token_model(self):
        token = Token(access_token="abc123xyz")
        assert token.access_token == "abc123xyz"
        assert token.token_type == "bearer"

    def test_token_model_custom_type(self):
        token = Token(access_token="abc123", token_type="custom")
        assert token.token_type == "custom"
