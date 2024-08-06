import os
from datetime import timedelta, datetime, UTC

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from ..schemas.auth import TokenPairSchema


# Определяем схему OAuth2 для получения токена
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

# СЕКРЕТНЫЙ КЛЮЧ ДЛЯ СОЗДАНИЯ СИГНАТУРЫ.
# Получаем из переменных окружения или используем значение по умолчанию
SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "default-i9i3902849209323m009sfhs90dh")

ALGORITHM = "HS512"  # Алгоритм шифрования, используемый для подписи токенов
USER_IDENTIFIER = "user_id"

# Время жизни access и refresh токенов
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_HOURS = 24 * 7


def create_jwt_token_pair(user_id: int) -> TokenPairSchema:
    """
    Создает пару токенов: access_token, refresh_token.
    :param user_id: Идентификатор пользователя.
    :return: :class:`TokenPair`.
    """
    # Создаем access_token с временем жизни ACCESS_TOKEN_EXPIRE_MINUTES минут
    access_token = _create_jwt_token(
        {USER_IDENTIFIER: user_id, "type": "access"},
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    # Создаем refresh_token с временем жизни REFRESH_TOKEN_EXPIRE_HOURS часов
    refresh_token = _create_jwt_token(
        {USER_IDENTIFIER: user_id, "type": "refresh"},
        timedelta(hours=REFRESH_TOKEN_EXPIRE_HOURS),
    )
    return TokenPairSchema(access_token=access_token, refresh_token=refresh_token)


def refresh_access_token(refresh_token: str) -> str:
    """
    Создает новый access_token на основе переданного refresh_token.
    """
    # Извлекаем полезную нагрузку из refresh_token и проверяем его тип
    payload = _get_token_payload(refresh_token, "refresh")

    # Создаем и возвращаем новый access_token на основе user_id из payload
    return _create_jwt_token(
        {USER_IDENTIFIER: payload[USER_IDENTIFIER], "type": "access"},
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )


def _create_jwt_token(data: dict, delta: timedelta) -> str:
    """
    Создает JWT токен с указанным временем жизни.

    :param data: Полезная нагрузка, которую нужно закодировать в токене.
    :param delta: Время жизни токена.
    :return: Закодированный JWT токен.
    """
    # Определяем время истечения токена
    expires_delta = datetime.now(UTC) + delta
    data.update({"exp": expires_delta})  # Добавляем время истечения в полезную нагрузку
    # Кодируем данные в JWT токен с использованием секретного ключа и алгоритма
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def _get_token_payload(token: str, token_type: str) -> dict:
    """
    Возвращает payload токена.

    :param token: Закодированный токен.
    :param token_type: Тип токена (access или refresh).
    :return: Словарь полезной нагрузки.
    :raises CredentialsException: Если токен недействителен.
    """
    try:
        # Декодируем токен, используя секретный ключ и алгоритм
        payload: dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        # Если декодирование не удалось, выбрасываем исключение HTTP 401 Unauthorized
        raise HTTPException(status_code=401, detail="Invalid token")

    # Проверяем, что тип токена соответствует ожидаемому
    if payload.get("type") != token_type:
        raise HTTPException(status_code=401, detail="Invalid token")
    # Проверяем, что идентификатор пользователя присутствует в payload
    if payload.get(USER_IDENTIFIER) is None:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    return payload
