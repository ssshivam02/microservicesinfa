from pydantic import BaseModel, EmailStr, conint, constr
from datetime import datetime


class Product_Schemas(BaseModel):
    name: str
    price: float
    quantity: int
    # this is because for giving dict type to pdantic model
    # this convert sqlalchemy into dict type
    class Config:
        orm_mode = True


class Product_Schemas_Out(BaseModel):
    id: int
    name: str
    added_at: datetime

    class Config:
        orm_mode = True
