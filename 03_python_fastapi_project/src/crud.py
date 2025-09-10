
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import Product
from schemas import ProductDTO, ProductCreate

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
