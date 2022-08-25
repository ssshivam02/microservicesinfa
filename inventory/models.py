from tkinter import Scale
from sqlalchemy.sql.expression import text
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base

# database migration we use


class Product_Table(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    price = Column(Float(precision=2, decimal_return_scale=None), nullable=False)
    quantity = Column(Integer, nullable=False)
    added_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
