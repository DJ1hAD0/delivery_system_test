from fastapi import Depends
from src import schemas, models
from sqlalchemy.orm import Session
from src.database import get_db


def get_region_by_name(region_name: str, db: Session = Depends(get_db)):
    result = db.query(models.Region).region_name.contains(search)).limit(limit).offset(skip).all()