from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.database import Base, engine
from database import models

from .api.prediction import router as prediction_router
from .api.pipelines import router as pipelines_router
from .api.analytics import router as analytics_router


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="AI-Based CI/CD Failure Prediction API",
    description="Machine learning API for predicting CI/CD pipeline failures.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "message": "AI-Based CI/CD Failure Prediction API is running."
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


app.include_router(prediction_router)
app.include_router(pipelines_router)
app.include_router(analytics_router)