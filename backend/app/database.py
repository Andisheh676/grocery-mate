# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# بارگذاری متغیرهای محیطی از فایل .env
load_dotenv()

# اتصال به دیتابیس (از .env خونده می‌شه، یا مقدار پیش‌فرض Docker Compose)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://admin:admin123@postgres:5432/devdb"
)

# ایجاد engine برای SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    connect_args={},  # اگر SQLite بود connect_args لازم بود، PostgreSQL نیازی نداره
)

# ساخت SessionLocal برای استفاده در dependencyهای FastAPI
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# پایه‌ی مدل‌ها (Base class)
Base = declarative_base()

# dependency برای گرفتن session دیتابیس در هر request
def get_db():
    """
    Provides a database session for FastAPI dependencies.
    Usage in routes:
        db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
