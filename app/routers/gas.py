import os
from typing import List
from fastapi import APIRouter
import pandas as pd
from pydantic import BaseModel
import uuid
from ..db import crud, schemas, models
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..dependencies import get_db

class GasData(BaseModel):
    gas1: List[int]
    gas2: List[int]
    gas3: List[int]
    gas4: List[int]
    gas5: List[int]
    gas6: List[int]
    gas7: List[int]
    gas8: List[int]
    gas9: List[int]
    temp: List[int]
    timestamp: List[int]

router = APIRouter(
    prefix="/gas",
    tags=["gas"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@router.get("/{id}", response_model=schemas.Gas)
def read_gas(id: int, db: Session = Depends(get_db)):
    db_gas = crud.get_gas(db=db, gas_id=id)
    if db_gas is None:
        raise HTTPException(status_code=404, detail="Gas Data not found")
    return db_gas

@router.get("/", response_model=List[schemas.Gas])
def read_gases(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    db_gases = crud.get_gases(db=db, skip=skip, limit=limit) 
    return db_gases

@router.post("/", response_model=schemas.Gas)
async def receive_gas_data(gas_data: GasData, db: Session = Depends(get_db)):
    data_unique_id = str(uuid.uuid4())
    # Ensure the output directory exists to stored data
    output_dir = "data_gases"
    os.makedirs(output_dir, exist_ok=True)

    # Create a DataFrame that combines all sensor data
    combined_df = pd.DataFrame({
        'timestamp': gas_data.timestamp,
        'gas1': gas_data.gas1,
        'gas2': gas_data.gas2,
        'gas3': gas_data.gas3,
        'gas4': gas_data.gas4,
        'gas5': gas_data.gas5,
        'gas6': gas_data.gas6,
        'gas7': gas_data.gas7,
        'gas8': gas_data.gas8,
        'gas9': gas_data.gas9,
        'temp': gas_data.temp
    })

    # Save the combined DataFrame to a single CSV file
    combined_file_path = os.path.join(output_dir, f'{data_unique_id}.csv')
    combined_df.to_csv(combined_file_path, index=False)

    # Save to the database to link with the data unique ID
    gas_schema = schemas.GasCreate(data_unique_id=data_unique_id)
    db_gas = crud.create_gas(db=db, gas=gas_schema)

    return db_gas