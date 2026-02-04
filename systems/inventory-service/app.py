from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Inventory Service")

class Product(BaseModel):
    id: str
    name: str
    stock: int

PRODUCTS = [
    Product(id="p1", name="Laptop", stock=10),
    Product(id="p2", name="Phone", stock=25),
    Product(id="p3", name="Tv", stock=12),
    Product(id="p4", name="Drives", stock=14),
    Product(id="p5", name="Keyboards", stock=31),
    Product(id="p6", name="GPU", stock=2),
]

@app.get("/products", response_model=List[Product])
def get_products():
    return PRODUCTS

@app.get("/health")
def health():
    return {"status": "ok",
            "service": "inventory-service"
            }