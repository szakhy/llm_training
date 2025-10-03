from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import CartDTO, CartItemAdd
from database import SessionLocal
from crud import get_cart, create_cart, add_item_to_cart, remove_item_from_cart, update_cart_item_quantity

router = APIRouter(prefix="/cart", tags=["cart"])

async def get_db():
    """
    Provide an AsyncSession database session for FastAPI dependency injection.
    
    This async generator yields an AsyncSession from SessionLocal and ensures the session is properly closed after use (context-managed). Intended to be used with Depends() in route handlers.
    """
    async with SessionLocal() as session:
        yield session

# For demo: use a single cart (id=1)
CART_ID = 1

@router.post("/create", response_model=CartDTO)
async def api_create_cart(db: AsyncSession = Depends(get_db)):
    """
    Create a new shopping cart and return it.
    
    Returns:
        CartDTO: The newly created cart.
    """
    cart = await create_cart(db)
    return cart

@router.get("/", response_model=CartDTO)
async def api_get_cart(db: AsyncSession = Depends(get_db)):
    """
    Retrieve the cart for the demo CART_ID.
    
    Returns:
        CartDTO: The cart data for the configured CART_ID.
    
    Raises:
        HTTPException: 404 if the cart does not exist.
    """
    cart = await get_cart(db, CART_ID)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart

@router.post("/add", response_model=CartDTO)
async def api_add_item(item: CartItemAdd, db: AsyncSession = Depends(get_db)):
    """
    Add an item to the demo cart and return the updated cart.
    
    Attempts to add the specified product and quantity to the demo cart (CART_ID = 1). Raises HTTPException 400 if the item cannot be added (e.g., out of stock or product not found).
    
    Parameters:
        item (CartItemAdd): Request body containing `product_id` and `quantity` to add.
    
    Returns:
        CartDTO: The cart after the item has been added.
    """
    added = await add_item_to_cart(db, CART_ID, item.product_id, item.quantity)
    if not added:
        raise HTTPException(status_code=400, detail="Cannot add item (out of stock or not found)")
    cart = await get_cart(db, CART_ID)
    return cart

@router.post("/remove", response_model=CartDTO)
async def api_remove_item(item: CartItemAdd, db: AsyncSession = Depends(get_db)):
    """
    Remove an item from the demo cart and return the updated cart.
    
    Removes the product identified by item.product_id from the cart (CART_ID). If the product is not present in the cart, raises HTTPException(status_code=404, detail="Item not in cart").
    
    Parameters:
        item (CartItemAdd): Request payload containing `product_id` of the item to remove. Only `product_id` is used.
    
    Returns:
        CartDTO: The updated cart after removal.
    """
    removed = await remove_item_from_cart(db, CART_ID, item.product_id)
    if not removed:
        raise HTTPException(status_code=404, detail="Item not in cart")
    cart = await get_cart(db, CART_ID)
    return cart

@router.post("/update", response_model=CartDTO)
async def api_update_quantity(item: CartItemAdd, db: AsyncSession = Depends(get_db)):
    """
    Update the quantity of a product in the demo cart and return the updated cart.
    
    Updates the item identified by item.product_id in the fixed demo cart (CART_ID = 1) to the provided quantity and returns the updated CartDTO.
    
    Parameters:
        item (CartItemAdd): Contains `product_id` and `quantity` for the update.
    
    Returns:
        CartDTO: The cart after the quantity update.
    
    Raises:
        HTTPException (400): If the update fails (product not found in cart or requested quantity unavailable).
    """
    updated = await update_cart_item_quantity(db, CART_ID, item.product_id, item.quantity)
    if not updated:
        raise HTTPException(status_code=400, detail="Cannot update quantity (out of stock or not found)")
    cart = await get_cart(db, CART_ID)
    return cart
