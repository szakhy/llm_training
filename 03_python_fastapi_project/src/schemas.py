
from pydantic import BaseModel
from typing import Optional

class ProductCreate(BaseModel):
    name: Optional[str] = None
    price: float
    description: Optional[str] = None
    stock: int


class ProductDTO(BaseModel):
    id: int
    name: str
    price: float
    description: Optional[str] = None
    stock: int

    class Config:
        orm_mode = True

