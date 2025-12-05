# Tutorial: Getting Started with Medical Records AI API

This tutorial will guide you through setting up and using the Medical Records AI API step by step.

## What You Will Learn

- How to install and run the API
- How to analyze patient symptoms using AI
- How to authenticate and save medical records

## Prerequisites

Before starting, make sure you have:

- Python 3.11 or higher installed
- Poetry package manager installed
- A MongoDB Atlas account (free tier works)
- A Groq API key (free)
- A Resend API key (free)

## Step 1: Clone the Repository

First, clone the project from GitHub:

```bash
git clone https://github.com/markrahimi/Medical_Records_AI_API.git
cd Medical_Records_AI_API
```

## Step 2: Install Dependencies

Use Poetry to install all required packages:

```bash
poetry install
```

This will create a virtual environment and install all dependencies.

## Step 3: Configure Environment Variables

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Open `.env` and fill in your credentials:

```env
MONGODB_URL=your_mongodb_connection_string
MONGODB_DB_NAME=medical_records
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.1-8b-instant
RESEND_API_KEY=your_resend_api_key
FROM_EMAIL=onboarding@resend.dev
SECRET_KEY=your_secret_key
```

## Step 4: Run the Server

Start the development server:

```bash
poetry run uvicorn app.main:app --reload
```

You should see output like:

```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Started reloader process
```

## Step 5: Test the API

### 5.1 Check if API is Running

Open your browser and go to: http://localhost:8000

You should see:

```json
{
  "message": "Welcome to Medical Records AI API",
  "version": "0.1.0",
  "docs": "/docs"
}
```

### 5.2 Analyze Patient Symptoms (Public Endpoint)

This endpoint does not require authentication. Use curl or any HTTP client:

```bash
curl -X POST http://localhost:8000/records/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "patient_name": "John Doe",
    "age": 30,
    "symptoms": "headache, fever, fatigue",
    "medical_history": null
  }'
```

The AI will analyze the symptoms and return recommendations:

```json
{
  "analysis": "Based on the symptoms of headache, fever, and fatigue...",
  "recommendations": [
    "Get plenty of rest",
    "Stay hydrated",
    "Monitor your temperature",
    "Consult a doctor if symptoms persist"
  ]
}
```

### 5.3 Interactive Documentation

Visit http://localhost:8000/docs to see the Swagger UI where you can test all endpoints interactively.

## Step 6: Authentication (Optional)

To save medical records, you need to authenticate:

### 6.1 Request OTP

```bash
curl -X POST http://localhost:8000/auth/request-otp \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Your Name",
    "email": "your.email@example.com"
  }'
```

Check your email for the OTP code.

### 6.2 Verify OTP and Get Token

```bash
curl -X POST http://localhost:8000/auth/verify-otp \
  -H "Content-Type: application/json" \
  -d '{
    "email": "your.email@example.com",
    "otp": "123456"
  }'
```

Save the `access_token` from the response.

### 6.3 Create a Medical Record

```bash
curl -X POST http://localhost:8000/records \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "patient_data": {
      "patient_name": "John Doe",
      "age": 30,
      "symptoms": "headache, fever",
      "medical_history": "none"
    }
  }'
```

## Summary

In this tutorial, you learned how to:

1. Install and configure the Medical Records AI API
2. Run the development server
3. Analyze patient symptoms using the public endpoint
4. Authenticate using OTP
5. Save medical records with authentication

## Next Steps

- Explore the API documentation at `/docs`
- Read the reference documentation in `docs/reference/`
- Check out the source code to understand the implementation

## Troubleshooting

**Server won't start?**
- Make sure all environment variables are set in `.env`
- Check that MongoDB connection string is correct

**AI analysis not working?**
- Verify your Groq API key is valid
- Check your Groq API quota

**Email not received?**
- Check your Resend API key
- Look in spam folder
