from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes.competitors import router as competitors_router
from app.api.routes.research import router as research_router

from app.database.connection import Base, engine
from app.database import models


@asynccontextmanager
async def lifespan(app: FastAPI):

    Base.metadata.create_all(bind=engine)

    yield


app = FastAPI(
    title="Competitor Intelligence Agent",
    description="Autonomous competitive research platform",
    version="0.3.0",
    lifespan=lifespan,
)


@app.get("/")
async def root():
    return {
        "application": "Competitor Intelligence Agent",
        "version": "0.3.0",
        "status": "running",
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


app.include_router(research_router)
app.include_router(competitors_router)