# 🏗 Project Architecture

## 1. Overview
Grocery Mate یک اپلیکیشن وب full-stack برای مدیریت لیست خرید و دستورهای آشپزی است.  
پروژه شامل دو بخش اصلی است: **backend** (FastAPI) و **frontend** (Vue.js).

## 2. Project Structure (Diagram)
نمودار ساختار پروژه در فایل Draw.io قرار دارد:  
[architecture.drawio](architecture.drawio)

## 3. Technologies
- Backend: Python + FastAPI
- Frontend: Vue.js, Vite, Axios
- Database: SQLite / MySQL
- Containerization: Docker, Docker Compose
- Version Control: Git + GitHub

## 4. Data Flow
1. Frontend درخواست‌ها را به Backend ارسال می‌کند.  
2. Backend منطق برنامه را پردازش کرده و با پایگاه داده کار می‌کند.  
3. پاسخ‌ها (JSON) به Frontend ارسال می‌شوند تا نمایش داده شوند.

## 5. Future Improvements
- اضافه کردن احراز هویت (JWT)  
- بهبود مدیریت خطا  
- اضافه کردن کشینگ (Redis)  
- راه‌اندازی CI/CD با GitHub Actions
