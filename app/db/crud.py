from sqlalchemy.orm import Session
from . import models, schemas

def get_gas(db: Session, gas_id: int):
    return db.query(models.Gas).filter(models.Gas.id == gas_id).first()

def get_gases(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Gas).offset(skip).limit(limit).all()

def create_gas(db: Session, gas: schemas.Gas):
    db_gas = models.Gas(
        data_unique_id = gas.data_unique_id
    )

    db.add(db_gas)
    db.commit()
    db.refresh(db_gas)
    return db_gas