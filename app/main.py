from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.core.database import close_mongo_connection, connect_to_mongo
from app.routes import auth, records


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()


app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    lifespan=lifespan
)

app.include_router(auth.router)
app.include_router(records.router)


@app.get("/")
async def root():
    return {
        "message": "Welcome to Medical Records AI API",
        "version": settings.version,
        "docs": "/docs"
    }
