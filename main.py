from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from typing import Optional
import secrets
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session


app = FastAPI(
    title="Products API",
    description="API for managing products",
    version="1.0.0",
    contact={
        "name": "Lucas Machi",
        "email": "lucascolafati@gmail.com"
    }
)

MY_USERNAME = "admin"
MY_PASSWORD = "admin"
DATABASE_URL = "sqlite:///./products.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
security = HTTPBasic()
Base = declarative_base()

class ProductDB(Base):
    __tablename__ = "products_table"
    id = Column(Integer, index=True, primary_key=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    available = Column(Boolean, default=True)

class Product(BaseModel):
    name: str
    description: str

Base.metadata.create_all(bind=engine)

def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    is_user_correct = secrets.compare_digest(credentials.username, MY_USERNAME)
    is_password_correct = secrets.compare_digest(credentials.password, MY_PASSWORD)

    if not (is_user_correct and is_password_correct):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Basic"}
        )

@app.post("/add")
def add_product(product: Product, db: Session = Depends(get_db_session), credentials: HTTPBasicCredentials = Depends(authenticate_user)):
    check_product_exists = db.query(ProductDB).filter(ProductDB.name == product.name, ProductDB.description == product.description).first()
    if check_product_exists:
        raise HTTPException(status_code=400, detail="This product already exists in the database!")

    new_product = ProductDB(name=product.name, description=product.description, available=True)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return {"message": "Product added successfully", "product": new_product}


@app.get("/products")
def list_products(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db_session),
    credentials: HTTPBasicCredentials = Depends(authenticate_user)
):
    if page < 1 or limit < 1:
        raise HTTPException(status_code=400, detail="Page or limit cannot be less than 1")

    listed_products = db.query(ProductDB).offset((page - 1) * limit).limit(limit).all()

    if not listed_products:
        return {"message": "There are no products"}

    total_products = db.query(ProductDB).count()

    return {
        "page": page,
        "limit": limit,
        "total": total_products,
        "products": [{"id": product.id, "name": product.name, "description": product.description} for product in listed_products]
    }


@app.put("/update/{product_id}")
def update_product(product_id: int, product: Product, db: Session = Depends(get_db_session), credentials: HTTPBasicCredentials = Depends(authenticate_user)):
    updated_product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
    if not updated_product:
        raise HTTPException(status_code=404, detail="This product does not exist in the database!")

    updated_product.name = product.name
    updated_product.description = product.description
    db.commit()
    db.refresh(updated_product)

    return {"message": "Product updated successfully!"}

# Route just to mark the product as unavailable
@app.patch("/update/{product_id}/unavailable")
def mark_unavailable(product_id: int, db: Session = Depends(get_db_session), credentials: HTTPBasicCredentials = Depends(authenticate_user)):
    product_stock_status = db.query(ProductDB).filter(ProductDB.id == product_id).first()
    if not product_stock_status:
        raise HTTPException(status_code=404, detail="This product does not exist in the database!")

    product_stock_status.available = False
    db.commit()
    db.refresh(product_stock_status)

    return {"message": "Product marked as unavailable", "product": product_stock_status}


@app.delete("/delete/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db_session), credentials: HTTPBasicCredentials = Depends(authenticate_user)):
    deleted_product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
    if not deleted_product:
        raise HTTPException(status_code=404, detail="This product does not exist in the database!")

    db.delete(deleted_product)
    db.commit()

    return {"message": "Product deleted successfully!"}
