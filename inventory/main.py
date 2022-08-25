from fastapi import FastAPI, Depends, HTTPException, status, Response
from fastapi.middleware.cors import CORSMiddleware
from . import models
from sqlalchemy.orm import Session
from inventory.database import engine, get_db
from inventory.models import Product_Table
from inventory.schemas import Product_Schemas, Product_Schemas_Out

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


@app.get("/products")
def all(db: Session = Depends(get_db)):
    # this will result all row with selected column
    # resall = db.query(Product_Table.name, Product_Table.quantity).all()
    # returns exactly one result or raises an exception (0 or more than 1 result)
    # resone = db.query(Product_Table.name).one() --> this will show error if in table multi row presnt
    # resone = db.query(Product_Table.name).one_or_none() -->this will show error if in table multi row presnt
    # res_scaler = db.query(Product_Table.name).scalar() --> only need one validation
    # # this will use filter
    res = db.query(Product_Table).filter(Product_Table.quantity <= 101).all()
    return res


@app.post("/product/create", response_model=Product_Schemas_Out)
def creat_product(product: Product_Schemas, db: Session = Depends(get_db)):
    new_product = Product_Table(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@app.delete("/product/delete/{id}")
def delete_product(id: str, db: Session = Depends(get_db)):
    product_query = db.query(Product_Table).filter(Product_Table.id == id)
    print("hello")
    post = product_query.first()
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with  id: {id} was not found",
        )

    product_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
