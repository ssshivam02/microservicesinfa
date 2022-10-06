from fastapi import FastAPI, Depends, HTTPException, status, Response
from fastapi.middleware.cors import CORSMiddleware
from . import models
from sqlalchemy.orm import Session
from .database import engine, get_db
from .models import Order_Table
from .schemas import Order_Schemas, Order_Schemas_Out
from starlette.requests import Request
import requests, time
from fastapi.background import BackgroundTasks
from inventory.database import get_db_inventory
from inventory.models import Product_Table

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


@app.get("/")
async def root(db: Session = Depends(get_db)):
    return {"message": " Hello World! "}


@app.post("/order/create", response_model=Order_Schemas_Out)
async def create_order(request: Request, db: Session = Depends(get_db)):
    new_order = await request.json()
    # print(request._json) this will print json body
    # print(type(request._json)) --->dict
    new_order = Order_Table(**new_order)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order


@app.get("/order/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    product_query = (
        db.query(Order_Table).filter(Order_Table.product_id == id).one_or_none()
    )
    post = product_query
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with  id: {id} was not found",
        )

    return product_query


@app.post("/order")
async def create(
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    db_inv: Session = Depends(get_db_inventory),
):
    body = await request.json()
    query_product = db_inv.query(Product_Table).filter(Product_Table.id == body["id"])
    if query_product.one().quantity < body["quantity"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Quantity with product_id:{body['id']} only this much quantity left {query_product.one().quantity}",
        )
    # this request is made for getting product by id

    req = requests.get("http://127.0.0.1:8000/product/%s" % body["id"])
    product = req.json()
    order = {
        "product_id": body["id"],
        "price": product["price"],
        "fee": 0.2 * product["price"],
        "total": product["price"] + 0.2 * product["price"],
        "quantity": body["quantity"],
        "status": "placed",
    }

    new_order = Order_Table(**order)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    background_tasks.add_task(order_completed, body, db, db_inv)
    return new_order


def order_completed(body, db, db_inv):
    time.sleep(5)  # after 30 sec we can see status is complete
    query = db.query(Order_Table).filter(Order_Table.product_id == body["id"])
    query.update({"status": "completed"}, synchronize_session=False)
    db.commit()
    query_product = db_inv.query(Product_Table).filter(Product_Table.id == body["id"])
    quantity = query_product.one().quantity - body["quantity"]
    query_product.update({"quantity": quantity})
    db_inv.commit()
    return query.first()


@app.delete("/order/delete/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    product_query = db.query(Order_Table).filter(Order_Table.product_id == id)
    post = product_query.first()
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with  id: {id} was not found",
        )

    product_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
