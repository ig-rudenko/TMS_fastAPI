from sqlalchemy.orm import Session

from ..schemas.auth import UserCreateSchema
from ..models import User


def create_user(session: Session, user: UserCreateSchema) -> User:
    """
    Создает пользователя в базе данных.
    :param session: Объект сессии с базой данных.
    :param user: Данные пользователя.
    :return: Объект модели пользователя.
    """
    # Преобразуем данные пользователя из схемы в объект модели пользователя
    user_model = User(**user.model_dump())

    session.add(user_model)  # Добавляем пользователя в сессию для последующего создания в базе.
    session.commit()  # Подтверждаем изменения, чтобы создать пользователя в базе.
    session.refresh(user_model)  # Обновляем объект пользователя, чтобы получить сгенерированный ID.
    return user_model
