# create_tables.py
from app.database import Base, engine
import app.models  # تمام مدل‌ها اینجا import می‌شن

# ساخت تمام جداول در دیتابیس
Base.metadata.create_all(bind=engine)

print("✅ All tables created successfully!")
