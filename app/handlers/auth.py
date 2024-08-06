from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_session
from app.models import User
from app.schemas.auth import UserCreateSchema, UserSchema, UserCredentialsSchema, TokenPairSchema, RefreshTokenSchema, \
    AccessTokenSchema
from app.services.auth import create_jwt_token_pair, refresh_access_token
from app.services.users import create_user, get_user_by_credentials, get_current_user

# Создаем роутер для маршрутов аутентификации с префиксом "/auth" и тегом "auth"
router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/users", response_model=UserSchema)
def register_user(
        user: UserCreateSchema, session: Session = Depends(get_session, use_cache=True)
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


@router.post("/token", response_model=TokenPairSchema)
async def get_tokens(user_data: UserCredentialsSchema, session: Session = Depends(get_session)):
    """Получение пары JWT"""
    user = await get_user_by_credentials(session, user_data.username, user_data.password)
    return create_jwt_token_pair(user_id=user.id)


@router.post("/token/refresh", response_model=AccessTokenSchema)
def refresh_token(token: RefreshTokenSchema):
    """Получение нового access token через refresh token"""
    return AccessTokenSchema(access_token=refresh_access_token(token.refresh_token))


@router.get("/me", response_model=UserSchema)
def get_current_user_view(current_user: User = Depends(get_current_user)):
    return current_user
