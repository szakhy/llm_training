
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import ProductDTO, ProductCreate
from database import SessionLocal
from crud import create_product as create_product_crud, get_products, get_product, update_product as update_product_crud, delete_product as delete_product_crud

router = APIRouter(prefix="/products", tags=["products"])

async def get_db():
    async with SessionLocal() as session:
        yield session

@router.post("/", response_model=ProductDTO)
async def create_product(product: ProductCreate, db: AsyncSession = Depends(get_db)):
    return await create_product_crud(db, product)

@router.get("/", response_model=list[ProductDTO])
async def read_products(db: AsyncSession = Depends(get_db)):
    return await get_products(db)

@router.get("/{product_id}", response_model=ProductDTO)
async def read_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await get_product(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=ProductDTO)
async def update_product(product_id: int, product: ProductCreate, db: AsyncSession = Depends(get_db)):
    updated_product = await update_product_crud(db, product_id, product.dict(exclude_unset=True))
    if updated_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product

@router.delete("/{product_id}")
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    deleted_product = await delete_product_crud(db, product_id)
    if deleted_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"detail": "Product deleted"}
