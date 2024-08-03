from fastapi import FastAPI
from app.handlers import auth

# Создаем экземпляр FastAPI для нашего веб-приложения
app = FastAPI()

# Подключаем роутер из модуля auth к основному приложению
# Все маршруты из auth.router будут доступны с префиксом "/api/v1"
app.include_router(auth.router, prefix="/api/v1")
