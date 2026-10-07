from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import health, resume, job, career, learning_interview, history
from app.db.session import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Safe database initialization: creates missing tables, never drops or deletes data
    init_db()
    yield


app = FastAPI(
    title="CareerIQ Backend",
    description="CareerIQ Backend API",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS for local development and production Vercel frontend
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://career-iq-ten.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API route modules
app.include_router(health.router, prefix="/api")
app.include_router(resume.router, prefix="/api")
app.include_router(job.router, prefix="/api")
app.include_router(career.router, prefix="/api")
app.include_router(learning_interview.router, prefix="/api")
app.include_router(history.router, prefix="/api")


@app.get("/")
async def root():
    return {
        "service": "CareerIQ Backend",
        "status": "online",
        "message": "Welcome to CareerIQ Backend API",
    }
