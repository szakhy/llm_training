
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Product, Cart, CartItem
from schemas import ProductDTO, ProductCreate
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
async def get_cart(db: AsyncSession, cart_id: int):
    result = await db.execute(
        select(Cart)
        .options(selectinload(Cart.items).selectinload(CartItem.product))
        .where(Cart.id == cart_id)
    )
    return result.scalars().first()

async def create_cart(db: AsyncSession):
    cart = Cart()
    db.add(cart)
    await db.commit()
    await db.refresh(cart)
    return cart

async def add_item_to_cart(db: AsyncSession, cart_id: int, product_id: int, quantity: int = 1):
    cart = await get_cart(db, cart_id)
    if not cart:
        return None
    # Check product availability
    product = await get_product(db, product_id)
    if not product or product.stock < quantity:
        return None
    # Check if item already in cart
    result = await db.execute(select(CartItem).where(and_(CartItem.cart_id == cart_id, CartItem.product_id == product_id)))
    item = result.scalars().first()
    if item:
        if product.stock < item.quantity + quantity:
            return None
        item.quantity += quantity
    else:
        item = CartItem(cart_id=cart_id, product_id=product_id, quantity=quantity)
        db.add(item)
    await db.commit()
    await db.refresh(item)
    return item

async def remove_item_from_cart(db: AsyncSession, cart_id: int, product_id: int):
    result = await db.execute(select(CartItem).where(and_(CartItem.cart_id == cart_id, CartItem.product_id == product_id)))
    item = result.scalars().first()
    if item:
        await db.delete(item)
        await db.commit()
        return True
    return False

async def update_cart_item_quantity(db: AsyncSession, cart_id: int, product_id: int, quantity: int):
    result = await db.execute(select(CartItem).where(and_(CartItem.cart_id == cart_id, CartItem.product_id == product_id)))
    item = result.scalars().first()
    if item:
        product = await get_product(db, product_id)
        if not product or product.stock < quantity:
            return None
        item.quantity = quantity
        await db.commit()
        await db.refresh(item)
        return item
    return None

async def get_product(db: AsyncSession, product_id: int):
    result = await db.execute(select(Product).where(Product.id == product_id))
    return result.scalars().first()

async def get_products(db: AsyncSession):
    result = await db.execute(select(Product))
    return result.scalars().all()

async def create_product(db: AsyncSession, product: ProductCreate):
    db_product = Product(**product.dict(exclude_unset=True))
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product

async def update_product(db: AsyncSession, product_id: int, product_data: dict):
    product = await get_product(db, product_id)
    if product:
        for key, value in product_data.items():
            setattr(product, key, value)
        await db.commit()
        await db.refresh(product)
    return product

async def delete_product(db: AsyncSession, product_id: int):
    product = await get_product(db, product_id)
    if product:
        await db.delete(product)
        await db.commit()
    return product
