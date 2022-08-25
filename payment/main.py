from urllib import request
from fastapi import FastAPI, Depends, HTTPException, status, Response
from fastapi.middleware.cors import CORSMiddleware
from . import models
from sqlalchemy.orm import Session
from payment.database import engine, get_db
from payment.models import Order_Table
from payment.schemas import Order_Schemas, Order_Schemas_Out
from starlette.requests import Request

app = FastAPI()
origins = [
    "https://www.google.com",
    "http://localhost:3000",
]  # this contain list of domain
# this is used to setup connection between frontend and this fastapi(backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # for public use ["*"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)


@app.post("/order/create", response_model=Order_Schemas_Out)
async def create_order(request: Request, db: Session = Depends(get_db)):
    new_order = await request.json()
    new_order = Order_Table(**new_order)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order
