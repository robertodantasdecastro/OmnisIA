"""API FastAPI para expor modelos treinados."""
from fastapi import FastAPI

app = FastAPI(title="OmnisIA")


@app.get("/")
async def root():
    return {"message": "OmnisIA API"}
