from pathlib import Path

from fastapi import FastAPI

from app.api.api_v1.api import api_router
from app.db.database import create_db_and_tables
from app.core.config import settings

BASE_PATH = Path(__file__).resolve().parent

app = FastAPI(title="BioTuring Public Notebook album server")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")