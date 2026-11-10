from fastapi import FastAPI

app = FastAPI(
    title="Competitor Intelligence Agent",
    description=(
        "An autonomous AI system for competitive "
        "research, monitoring and intelligence."
    ),
    version="0.1.0",
)


@app.get("/")
async def root():
    return {
        "application": "Competitor Intelligence Agent",
        "version": "0.1.0",
        "status": "running",
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "competitor-intelligence-agent",
    }