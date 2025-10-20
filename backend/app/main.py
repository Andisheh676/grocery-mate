from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import auth, ingredients, shopping_lists, recipes, admin, news

# ابتدا دیتابیس بساز
Base.metadata.create_all(bind=engine)

# ایجاد اپلیکیشن
app = FastAPI(
    title="GroceryMate API",
    description="API for managing groceries, shopping lists, and recipes",
    version="1.0.0"
)

# فعال کردن CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# اضافه کردن router ها
app.include_router(auth.router)  # مسیرها: /auth/register, /auth/login
app.include_router(ingredients.router)
app.include_router(shopping_lists.router)  # فقط router بدون prefix
app.include_router(recipes.router)
app.include_router(admin.router)
app.include_router(news.router)


# روت اصلی
@app.get("/")
def read_root():
    return {
        "message": "Welcome to GroceryMate API",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
