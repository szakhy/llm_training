from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Product, Cart, CartItem
from schemas import ProductDTO, ProductCreate
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
async def get_cart(db: AsyncSession, cart_id: int):
    """
    Retrieve a Cart by ID, eagerly loading its items and each item's associated Product.
    
    Retrieves the Cart with the given cart_id using eager loading (selectinload) to load Cart.items and each CartItem.product in the same query.
    
    Parameters:
        cart_id (int): ID of the cart to fetch.
    
    Returns:
        Cart | None: The Cart instance with populated items and products, or None if no cart with that ID exists.
    """
    result = await db.execute(
        select(Cart)
        .options(selectinload(Cart.items).selectinload(CartItem.product))
        .where(Cart.id == cart_id)
    )
    return result.scalars().first()

async def create_cart(db: AsyncSession):
    """
    Create and persist a new Cart in the database.
    
    Creates a Cart instance, adds it to the provided AsyncSession, commits the transaction,
    and refreshes the instance so generated fields (e.g., id, timestamps) are populated.
    
    Returns:
        Cart: The newly created and refreshed Cart object.
    """
    cart = Cart()
    db.add(cart)
    await db.commit()
    await db.refresh(cart)
    return cart

async def add_item_to_cart(db: AsyncSession, cart_id: int, product_id: int, quantity: int = 1):
    """
    Add a product to a cart, creating a new CartItem or incrementing an existing one.
    
    If the cart or product doesn't exist, or if the product's stock is insufficient for the requested addition, the function returns None. On success it either creates a new CartItem with the requested quantity or increases the quantity of an existing CartItem, commits the transaction, refreshes the item, and returns the persisted CartItem.
    
    Parameters:
        cart_id (int): ID of the cart to modify.
        product_id (int): ID of the product to add.
        quantity (int, optional): Quantity to add (default 1).
    
    Returns:
        CartItem | None: The created or updated CartItem on success, or None if the cart/product is missing or stock is insufficient.
    """
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
    """
    Remove a specific product item from a cart.
    
    Attempts to find the CartItem matching the given cart_id and product_id; if found, deletes it from the database and commits the transaction.
    
    Parameters:
        cart_id (int): ID of the cart containing the item.
        product_id (int): ID of the product to remove from the cart.
    
    Returns:
        bool: True if an item was found and removed; False if no matching item existed.
    """
    result = await db.execute(select(CartItem).where(and_(CartItem.cart_id == cart_id, CartItem.product_id == product_id)))
    item = result.scalars().first()
    if item:
        await db.delete(item)
        await db.commit()
        return True
    return False

async def update_cart_item_quantity(db: AsyncSession, cart_id: int, product_id: int, quantity: int):
    """
    Update the quantity of an existing CartItem in a cart after validating product stock.
    
    If the cart item exists and the product has at least `quantity` units in stock, the item's quantity
    is set to `quantity`, the change is committed, and the refreshed CartItem is returned. Returns
    None if the cart item or product is not found, or if the product's stock is insufficient.
    
    Parameters:
        cart_id (int): ID of the cart that contains the item.
        product_id (int): ID of the product whose cart item quantity will be updated.
        quantity (int): New desired quantity for the cart item.
    
    Returns:
        CartItem | None: The updated CartItem on success, otherwise None.
    """
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
    """
    Retrieve a Product by its primary key.
    
    Parameters:
        product_id (int): ID of the product to fetch.
    
    Returns:
        Product | None: The Product instance if found, otherwise None.
    """
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
