import schemas
from database import engine,SessionLocal
import datetime
from sqlalchemy.orm import Session
import models


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




