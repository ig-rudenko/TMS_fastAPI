from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from fastapi import Depends, HTTPException

from app.database import get_session
from app.models import User
from app.schemas.auth import UserCreateSchema
from app.services.auth import _get_token_payload, oauth2_scheme, USER_IDENTIFIER
from app.services.encrypt import encrypt_password, validate_password


def create_user(session: Session, user: UserCreateSchema) -> User:
    """
    Создает пользователя в базе данных.
    :param session: Объект сессии с базой данных.
    :param user: Данные пользователя.
    :return: Объект модели пользователя.
    """
    # Преобразуем данные пользователя из схемы в объект модели пользователя
    user_model = User(**user.model_dump())
    # Шифруем пароль
    user_model.password = encrypt_password(user_model.password)

    session.add(user_model)  # Добавляем пользователя в сессию для последующего создания в базе.
    session.commit()  # Подтверждаем изменения, чтобы создать пользователя в базе.
    session.refresh(user_model)  # Обновляем объект пользователя, чтобы получить сгенерированный ID.
    return user_model


def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session, use_cache=True),
) -> User:
    """
    Получение текущего пользователя по токену аутентификации.

    :param token: Токен пользователя, извлекаемый через зависимость oauth2_scheme.
    :param session: Объект сессии для взаимодействия с базой данных, создается через зависимость get_session.
    :return: Объект пользователя User.
    :raises HTTPException: Если пользователь не найден или токен недействителен.
    """
    # Извлекаем полезную нагрузку из токена и проверяем его тип
    payload = _get_token_payload(token, "access")

    try:
        # Формируем запрос для получения пользователя из базы данных по его ID
        query = select(User).where(User.id == payload[USER_IDENTIFIER])
        print(query)
        result = session.execute(query)  # Выполняем запрос
        result.unique()  # Убедиться, что результат уникален (одна запись)

        # Извлекаем объект пользователя из результата запроса
        return result.scalar_one()  # Если запись найдена, возвращаем объект User

    except NoResultFound:
        # Если пользователь не найден, выбрасываем исключение HTTP 401 Unauthorized
        raise HTTPException(status_code=401, detail="Could not validate credentials")


async def get_user_by_credentials(session: Session, username: str, password: str) -> User:
    """
    Получение пользователя по его учетным данным (имя пользователя и пароль).

    :param session: Объект сессии для взаимодействия с базой данных.
    :param username: Имя пользователя.
    :param password: Пароль пользователя.
    :return: Объект пользователя User.
    :raises HTTPException: Если пользователь не найден или учетные данные недействительны.
    """
    try:
        # Формируем запрос для получения пользователя из базы данных по его имени пользователя
        query = select(User).where(User.username == username)
        print(query)
        result = session.execute(query)  # Выполняем запрос
        result.unique()  # Убедиться, что результат уникален (одна запись)
        # Извлекаем объект пользователя из результата запроса
        user = result.scalar_one()  # Если запись найдена, присваиваем объект User переменной user

    except NoResultFound:
        # Если пользователь не найден, выбрасываем исключение HTTP 401 Unauthorized
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    # Проверяем, соответствует ли введенный пароль захешированному паролю из базы данных
    if not validate_password(password, user.password):
        # Если пароли не совпадают, выбрасываем исключение HTTP 401 Unauthorized
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    # Если все проверки пройдены, возвращаем объект пользователя
    return user
