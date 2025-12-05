import json
import re

from groq import Groq

from app.core.config import settings
from app.models.medical_record import MedicalAnalysis, PatientData


class AIService:
    def __init__(self):
        self.client = Groq(api_key=settings.groq_api_key)

    async def analyze_patient_data(self, patient_data: PatientData) -> MedicalAnalysis:
        prompt = f"""You are a medical assistant. Analyze the following patient information and provide:
1. A brief medical analysis
2. A list of recommendations

Patient Information:
- Name: {patient_data.patient_name}
- Age: {patient_data.age}
- Symptoms: {patient_data.symptoms}
- Medical History: {patient_data.medical_history or 'None'}

Please respond in JSON format:
{{
    "analysis": "your analysis here",
    "recommendations": ["recommendation 1", "recommendation 2", ...]
}}

IMPORTANT: Provide general health advice only. This is not a substitute for professional medical diagnosis."""

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful medical assistant providing general health information.",
                    },
                    {"role": "user", "content": prompt},
                ],
                model=settings.groq_model,
                temperature=0.7,
                max_tokens=1024,
            )

            response_text = chat_completion.choices[0].message.content
            json_match = re.search(r"\{.*\}", response_text, re.DOTALL)

            if json_match:
                result = json.loads(json_match.group())
                return MedicalAnalysis(**result)
            else:
                return MedicalAnalysis(
                    analysis=response_text,
                    recommendations=["Consult with a healthcare professional"],
                )

        except Exception:
            return MedicalAnalysis(
                analysis="Unable to analyze at this time. Please try again later.",
                recommendations=["Consult with a healthcare professional if symptoms persist"],
            )


ai_service = AIService()
