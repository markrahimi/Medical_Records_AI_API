# Medical Records AI API

https://github.com/markrahimi/Medical_Records_AI_API

A FastAPI-based medical records management system with AI-powered patient data analysis using Groq AI. Features OTP-based authentication via email and MongoDB Atlas for data persistence.

## Features

- **AI-Powered Analysis**: Analyze patient symptoms using Groq's LLaMA models
- **OTP Authentication**: Secure email-based OTP login system via Resend
- **Medical Records Management**: Store and retrieve patient records with AI analysis
- **Public & Authenticated Endpoints**: Public analysis without storage, authenticated record keeping
- **MongoDB Atlas Integration**: Cloud-based NoSQL database for scalability

## Technology Stack

- **Backend Framework**: FastAPI
- **Database**: MongoDB Atlas (cloud)
- **AI Service**: Groq API (LLaMA 3.1)
- **Email Service**: Resend
- **Authentication**: JWT tokens with OTP verification
- **Build Tool**: Poetry
- **Server**: Uvicorn (ASGI)

## Project Structure

```
+ app/

      -core/
          -- config.py          # Environment configuration
          -- database.py        # MongoDB connection
      - models/
          -- user.py            # User and auth models
          -- medical_record.py  # Medical record models
      - routes/
          -- auth.py            # Authentication endpoints
          -- records.py         # Medical records endpoints
      - services/
          -- ai_service.py      # Groq AI integration
          -- email_service.py   # Resend email integration
          -- auth_service.py    # OTP and JWT handling
+ tests/                        # Test Directory
    -- conftest.py
    -- test_api.py
+ main.py                       # FastAPI application
+ pyproject.toml                # Poetry dependencies
+ .env.example                  # Environment variables template
+ .gitignore
+ README.md
```

## Prerequisites

- Python 3.11+
- Poetry (Python package manager)
- MongoDB Atlas account
- Groq API key
- Resend account with API key

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/markrahimi/Medical_Records_AI_API
cd Medical_Records_AI_API
```

### 2. Install Dependencies

```bash
poetry install
```

### 3. Environment Configuration

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/?appName=yourapp
MONGODB_DB_NAME=medical_records

GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.1-8b-instant

RESEND_API_KEY=your_resend_api_key_here
FROM_EMAIL=onboarding@resend.dev

SECRET_KEY=your-secret-key-here
```

#### Getting API Keys:

**MongoDB Atlas**:

1. Sign up at https://www.mongodb.com/cloud/atlas
2. Create a free cluster
3. Go to Database Access → Add Database User
4. Go to Network Access → Add IP Address (allow from anywhere for testing)
5. Get connection string from Databases → Connect → Drivers

**Groq API**:

1. Sign up at https://console.groq.com/
2. Navigate to API Keys
3. Create new API key

**Resend API**:

1. Sign up at https://resend.com/signup
2. Navigate to API Keys
3. Create new API key
4. Free tier: 100 emails/day

## Running the Application

### Development Server

```bash
poetry run uvicorn app.main:app --reload
```

The API will be available at: http://localhost:8000

### API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Public Endpoints

#### `GET /`

Health check and API information.

**Response**:

```json
{
  "message": "Welcome to Medical Records AI API",
  "version": "0.1.0",
  "docs": "/docs"
}
```

#### `POST /records/analyze`

Analyze patient data without saving (no authentication required).

**Request Body**:

```json
{
  "patient_name": "John Doe",
  "age": 35,
  "symptoms": "headache, fever, cough",
  "medical_history": "diabetes type 2"
}
```

**Response**:

```json
{
  "analysis": "Based on the symptoms...",
  "recommendations": [
    "Get plenty of rest",
    "Stay hydrated",
    "Consult a healthcare professional"
  ]
}
```

### Authentication Endpoints

#### `POST /auth/request-otp`

Request OTP code via email.

**Request Body**:

```json
{
  "name": "John Doe",
  "email": "john@example.com"
}
```

**Response**:

```json
{
  "message": "OTP sent to john@example.com"
}
```

#### `POST /auth/verify-otp`

Verify OTP and receive JWT token.

**Request Body**:

```json
{
  "email": "john@example.com",
  "otp": "123456"
}
```

**Response**:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Authenticated Endpoints

**Note**: All authenticated endpoints require `Authorization: Bearer <token>` header.

#### `POST /records`

Create and save a medical record with AI analysis.

**Headers**:

```
Authorization: Bearer <your_jwt_token>
```

**Request Body**:

```json
{
  "patient_data": {
    "patient_name": "Jane Smith",
    "age": 28,
    "symptoms": "back pain, fatigue",
    "medical_history": null
  }
}
```

**Response**:

```json
{
  "id": "507f1f77bcf86cd799439011",
  "patient_data": { ... },
  "ai_analysis": {
    "analysis": "...",
    "recommendations": [...]
  },
  "created_at": "2025-11-14T10:30:00Z",
  "user_id": "507f1f77bcf86cd799439012"
}
```

#### `GET /records`

Retrieve all medical records (accessible to all authenticated users).

**Headers**:

```
Authorization: Bearer <your_jwt_token>
```

**Response**:

```json
[
  {
    "id": "507f1f77bcf86cd799439011",
    "patient_data": { ... },
    "ai_analysis": { ... },
    "created_at": "2025-11-14T10:30:00Z",
    "user_id": "507f1f77bcf86cd799439012"
  }
]
```

## Usage Example

### 1. Test Public Analysis (No Auth)

```bash
curl -X POST http://localhost:8000/records/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "patient_name": "Test Patient",
    "age": 30,
    "symptoms": "headache, fever",
    "medical_history": null
  }'
```

### 2. Request OTP

```bash
curl -X POST http://localhost:8000/auth/request-otp \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Your Name",
    "email": "your.email@example.com"
  }'
```

Check your email for the OTP code.

### 3. Verify OTP and Get Token

```bash
curl -X POST http://localhost:8000/auth/verify-otp \
  -H "Content-Type: application/json" \
  -d '{
    "email": "your.email@example.com",
    "otp": "123456"
  }'
```

Save the `access_token` from the response.

### 4. Create a Record (Authenticated)

```bash
curl -X POST http://localhost:8000/records \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "patient_data": {
      "patient_name": "John Doe",
      "age": 45,
      "symptoms": "chest pain, shortness of breath",
      "medical_history": "hypertension"
    }
  }'
```

### 5. Get All Records (Authenticated)

```bash
curl -X GET http://localhost:8000/records \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Build Tool - Poetry

This project uses **Poetry** as the modern Python build tool for complete project lifecycle management.

### Why Poetry?

Poetry provides a unified solution for:

- **Dependency Management**: Automatic resolution and locking of dependencies
- **Virtual Environment Management**: Isolated Python environments
- **Project Packaging**: Build wheels and source distributions
- **Version Management**: Centralized version control in `pyproject.toml`
- **Script Execution**: Run scripts in isolated environments

### Build Tool Automation Tasks

#### 1. Dependency Management

Poetry automatically manages all project dependencies with version constraints:

```bash
# Install all dependencies from pyproject.toml
poetry install

# Add a new dependency
poetry add fastapi

# Add a development dependency
poetry add --group dev pytest

# Update dependencies
poetry update

# Show dependency tree
poetry show --tree
```

All dependencies are locked in `poetry.lock` to ensure reproducible builds across different environments.

#### 2. Project Version Management

Version is centrally managed in `pyproject.toml`:

```toml
[project]
version = "0.1.0"
```

Update version:

```bash
poetry version patch  # 0.1.0 -> 0.1.1
poetry version minor  # 0.1.0 -> 0.2.0
poetry version major  # 0.1.0 -> 1.0.0
```

#### 3. Packaging & Distribution

Build distributable packages (wheels and source distributions):

```bash
# Build package
poetry build

# Output:
# - dist/medical_records_api-0.1.0-py3-none-any.whl
# - dist/medical_records_api-0.1.0.tar.gz
```

Publish to PyPI (when ready):

```bash
poetry publish
```

#### 4. Script Execution

Run application in isolated virtual environment:

```bash
# Run FastAPI server
poetry run uvicorn app.main:app --reload

# Run Python scripts
poetry run python -m app.main

# Execute any command in virtualenv
poetry run python --version
```

### Key Poetry Commands

```bash
# Install dependencies
poetry install

# Add new dependency
poetry add package-name

# Update dependencies
poetry update

# Run application
poetry run uvicorn app.main:app --reload

# Show installed packages
poetry show

# Build package (creates .whl and .tar.gz)
poetry build

# Manage versions
poetry version patch
```

### Dependencies Management

All dependencies are defined in `pyproject.toml`:

- **fastapi**: Web framework
- **uvicorn**: ASGI server
- **motor**: Async MongoDB driver
- **pymongo**: MongoDB driver
- **pydantic-settings**: Environment configuration
- **python-jose**: JWT handling
- **passlib**: Password utilities
- **groq**: Groq AI client
- **resend**: Email service
- **python-multipart**: Form data handling
- **email-validator**: Email validation for Pydantic

### Replicable Builds

The build process is fully reproducible:

1. **Clone repository**
2. **Run `poetry install`** - installs exact versions from `poetry.lock`
3. **Configure `.env`** - set environment variables
4. **Run `poetry run uvicorn app.main:app`** - start application

This ensures identical environments across development, testing, and production.

## Project Metadata

Project metadata is managed in `pyproject.toml`:

```toml
[project]
name = "medical-records-api"
version = "0.1.0"
description = "Medical Records AI Analysis API with FastAPI"
authors = [
    {name = "Mark Rahimi", email = "markrahimi@example.com"}
]
requires-python = "^3.11"
```

## Development

### Code Structure

- **Models**: Pydantic models for request/response validation
- **Routes**: API endpoint definitions
- **Services**: Business logic (AI, email, auth)
- **Core**: Configuration and database connection

### Adding New Features

1. Define models in `app/models/`
2. Create service logic in `app/services/`
3. Add routes in `app/routes/`
4. Register router in `app/main.py`

## Testing

This project includes automated tests using pytest.

### Running Tests

```bash
poetry run pytest
```

Run with verbose output:

```bash
poetry run pytest -v
```

Run with coverage:

```bash
poetry run pytest --cov=app
```

### Test Structure

```
tests/
    ─ __init__.py
    ─ conftest.py      # Pytest fixtures
    ─ test_api.py      # API endpoint tests
```

### Test Coverage

Current tests cover:

- ✅ Root endpoint (`/`)
- ✅ Public analyze endpoint (`/records/analyze`)
- ✅ OTP request endpoint (`/auth/request-otp`)
- ✅ OTP verification (`/auth/verify-otp`)
- ✅ Protected routes authentication
- ✅ Invalid token handling

### Writing New Tests

Example test:

```python
@pytest.mark.asyncio
async def test_new_endpoint(client: AsyncClient):
    response = await client.get("/endpoint")
    assert response.status_code == 200
```

## Security Notes

- Never commit `.env` file to version control
- Use strong `SECRET_KEY` in production
- Keep Resend API key secure
- Restrict MongoDB network access in production
- OTP storage is in-memory (use Redis for production)
- JWT tokens expire after 60 minutes by default

## Troubleshooting

**MongoDB Connection Error**:

- Verify connection string in `.env`
- Check network access settings in MongoDB Atlas
- Ensure correct database user credentials

**Email Not Sending**:

- Verify Resend API key is correct
- Check Resend account status
- Ensure `FROM_EMAIL` is valid (use `onboarding@resend.dev` for testing)
- Check Resend dashboard for error logs

**Groq API Error**:

- Verify API key is valid
- Check Groq API quota/limits
- Ensure model name is correct

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/markrahimi/Medical_Records_AI_API/blob/main/LICENSE) file for details.

## Author

Mohammadali RAHIMI KOUHBANANI (MARKRAHIMI) - Technological foundations of software development
