from typing import Generator
from app.db.database import SessionLocal

def get_session() -> Generator:
    db = SessionLocal()
    db.current_user_id = None
    try:
        yield db
    finally:
        db.close()
