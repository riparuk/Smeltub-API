from pydantic import BaseModel

class GasBase(BaseModel):
    id: int

class Gas(GasBase):
    data_unique_id: str

    class Config:
        from_attributes = True

class GasCreate(BaseModel):
    data_unique_id: str

