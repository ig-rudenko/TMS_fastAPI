from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session

# URL базы данных SQLite, указывающий на файл базы данных 'test.db' в текущей директории.
# Три слэша в данном случае обязательны.
DATABASE_URL = "sqlite:///./test.db"

# Создаем движок для подключения к базе данных, который управляет пулом подключений и диалектом SQL.
# `create_engine` создаёт объект Engine, который используется для взаимодействия с базой данных.
engine = create_engine(DATABASE_URL, echo=True)

# Создаем фабрику сессий для взаимодействия с базой данных.
# `sessionmaker` возвращает объект класса, который можно использовать для создания сессий.
# `autocommit=False` означает, что изменения в базе данных не будут автоматически подтверждаться.
# `autoflush=False` означает, что изменения не будут автоматически записываться в базу данных до явного вызова commit().
# `bind=engine` связывает фабрику сессий с конкретным движком базы данных.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """
    Декларативный базовый класс для моделей.

    https://docs.sqlalchemy.org/en/20/orm/declarative_styles.html
    """

    pass


def get_session() -> Generator[Session]:
    """
    Генератор, который создает сессию для взаимодействия с базой данных
    и автоматически закрывает её после завершения работы.
    :return: Сессия базы данных
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
