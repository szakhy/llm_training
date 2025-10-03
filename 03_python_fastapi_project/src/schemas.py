
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

# --- Cart Schemas ---
from typing import List

class CartItemDTO(BaseModel):
    id: int
    product: ProductDTO
    quantity: int

    class Config:
        orm_mode = True

class CartDTO(BaseModel):
    id: int
    items: List[CartItemDTO]

    class Config:
        orm_mode = True

class CartItemAdd(BaseModel):
    product_id: int
    quantity: int = 1

