
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import products
from routes import cart
from database import engine, Base

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    """
    On startup, create all tables including Cart and CartItem if not present.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(products.router)
app.include_router(cart.router)
