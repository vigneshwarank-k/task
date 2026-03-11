from fastapi import HTTPException, APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db.database import get_db
from models.models import Products

router = APIRouter()


class CreateProduct(BaseModel):
    name: str
    price: float
    stock: int
    aisle: str


@router.post("/create-product")
def create_products(data: CreateProduct, db: Session = Depends(get_db)):
    try:
        response = Products(**data.model_dump())
        db.add(response)
        db.commit()
        db.refresh(response)
        return {"status": "success", "data": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/getall-products")
def create_products(db: Session = Depends(get_db)):
    try:
        datas = db.query(Products).all()
        return {"status": "success", "data": datas}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
