from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import CartDTO, CartItemAdd
from database import SessionLocal
from crud import get_cart, create_cart, add_item_to_cart, remove_item_from_cart, update_cart_item_quantity

router = APIRouter(prefix="/cart", tags=["cart"])

async def get_db():
    async with SessionLocal() as session:
        yield session

# For demo: use a single cart (id=1)
CART_ID = 1

@router.post("/create", response_model=CartDTO)
async def api_create_cart(db: AsyncSession = Depends(get_db)):
    cart = await create_cart(db)
    return cart

@router.get("/", response_model=CartDTO)
async def api_get_cart(db: AsyncSession = Depends(get_db)):
    cart = await get_cart(db, CART_ID)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart

@router.post("/add", response_model=CartDTO)
async def api_add_item(item: CartItemAdd, db: AsyncSession = Depends(get_db)):
    added = await add_item_to_cart(db, CART_ID, item.product_id, item.quantity)
    if not added:
        raise HTTPException(status_code=400, detail="Cannot add item (out of stock or not found)")
    cart = await get_cart(db, CART_ID)
    return cart

@router.post("/remove", response_model=CartDTO)
async def api_remove_item(item: CartItemAdd, db: AsyncSession = Depends(get_db)):
    removed = await remove_item_from_cart(db, CART_ID, item.product_id)
    if not removed:
        raise HTTPException(status_code=404, detail="Item not in cart")
    cart = await get_cart(db, CART_ID)
    return cart

@router.post("/update", response_model=CartDTO)
async def api_update_quantity(item: CartItemAdd, db: AsyncSession = Depends(get_db)):
    updated = await update_cart_item_quantity(db, CART_ID, item.product_id, item.quantity)
    if not updated:
        raise HTTPException(status_code=400, detail="Cannot update quantity (out of stock or not found)")
    cart = await get_cart(db, CART_ID)
    return cart
