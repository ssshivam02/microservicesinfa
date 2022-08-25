from os import stat_result
from pydantic import BaseModel, EmailStr, conint, constr
from datetime import datetime


class Order_Schemas(BaseModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str
    # this is because for giving dict type to pdantic model
    # this convert sqlalchemy into dict type
    class Config:
        orm_mode = True


class Order_Schemas_Out(BaseModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str
    ordered_at: datetime

    class Config:
        orm_mode = True
