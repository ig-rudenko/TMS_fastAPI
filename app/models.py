from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from .database import Base  # Импортируем базовый класс для моделей из нашего модуля database


class User(Base):
    __tablename__ = 'users'  # Указываем имя таблицы для модели User

    # Колонки таблицы
    id: Mapped[int] = mapped_column(primary_key=True)  # Первичный ключ типа Integer
    username: Mapped[str] = mapped_column(String(50), unique=True)
    password: Mapped[str] = mapped_column(String(150))
    email: Mapped[str] = mapped_column(String(256), unique=True)

    # Связи
    # Отношение "один ко многим" с таблицей Post.
    # `lazy="select"` означает, что связанные объекты Post будут подгружены, когда к ним будет обращение.
    posts = relationship('Post', back_populates='user', lazy="select")


class Post(Base):
    __tablename__ = 'posts'  # Указываем имя таблицы для модели Post

    # Колонки таблицы
    id: Mapped[int] = mapped_column(primary_key=True)  # Первичный ключ типа Integer
    title: Mapped[str] = mapped_column(String(256))
    content: Mapped[str] = mapped_column(Text)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))

    # Связи
    # Отношение "многие к одному" с таблицей User.
    user: Mapped[User] = relationship('User', back_populates='posts')
