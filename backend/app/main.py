from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.database import engine, Base
from app.routers import auth, ingredients, shopping_lists, recipes, admin, news
from dotenv import load_dotenv
import os

# --------------------------
# Load environment variables
# --------------------------
load_dotenv("/root/grocery-mate/backend/.env")  # حتما قبل از استفاده

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY is None:
    raise ValueError("GEMINI_API_KEY not found in .env")

# --------------------------
# Initialize database
# --------------------------
Base.metadata.create_all(bind=engine)

# --------------------------
# Create FastAPI app
# --------------------------

origins = [
    "http://localhost:5173",  # پورت frontend
    "http://91.99.23.49:5173",  # اگر با IP خارجی دسترسی داری
]

app = FastAPI(
    title="GroceryMate API",
    description="API for managing groceries, shopping lists, and recipes",
    version="1.0.0"
)

# --------------------------
# Enable CORS
# --------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------
# Include routers
# --------------------------
app.include_router(auth.router)          # مسیرها: /auth/register, /auth/login
app.include_router(ingredients.router)
app.include_router(shopping_lists.router)
app.include_router(recipes.router)
app.include_router(admin.router)
app.include_router(news.router)

# --------------------------
# Root endpoint
# --------------------------
@app.get("/")
def read_root():
    return {
        "message": "Welcome to GroceryMate API",
        "docs": "/docs",
        "redoc": "/redoc"
    }

# --------------------------
# Health check endpoint
# --------------------------
@app.get("/health")
def health_check():
    return {"status": "healthy"}
