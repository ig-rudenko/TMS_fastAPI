from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_session
from app.schemas.auth import UserCreateSchema, UserSchema
from app.services.auth import create_user

# Создаем роутер для маршрутов аутентификации с префиксом "/auth" и тегом "auth"
router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/users", response_model=UserSchema)
def register_user(
        user: UserCreateSchema, session: Session = Depends(get_session)
):
    """
    Регистрация нового пользователя.

    Depends(get_session) говорит FastAPI использовать функцию get_session для создания
    и предоставления объекта Session при вызове register_user. Это позволяет управлять
    сессией базы данных и её закрытием без необходимости вручную передавать или закрывать её в функции.

    :param user: Объект данных пользователя для регистрации, должен соответствовать UserCreateSchema.
    :param session: Объект сессии базы данных, используемый для выполнения операций с базой данных.
                    Значение по умолчанию устанавливается через зависимость (Depends) от функции get_session.
    """
    try:
        # Пытаемся создать нового пользователя с использованием переданных данных
        return create_user(session, user)
    except IntegrityError:
        # Если возникает ошибка уникальности (например, пользователь с таким username или email уже существует),
        # выбрасываем исключение HTTP 422 с соответствующим сообщением.
        raise HTTPException(status_code=422, detail="User already exists")
