from sqlalchemy import String, Text, ForeignKey, Table, Column, Integer
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


# Определяем вспомогательную таблицу для связи "многие ко многим" между Post и Tag
posts_tag_table = Table(
    "posts_tags_table",
    Base.metadata,  # Метаданные базы данных, необходимые для декларативного определения таблицы
    Column("id", Integer, primary_key=True),
    Column("posts_id", Integer, ForeignKey("posts.id", ondelete="CASCADE")),
    # `ondelete="CASCADE"` означает, что при удалении записи в таблице posts все связанные записи
    # в этой вспомогательной таблице также будут удалены
    Column("tags_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"))
)


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
    # Отношение "многие ко многим" с таблицей Tag.
    tags = relationship('Tag', back_populates='posts', lazy="select", secondary=posts_tag_table)
    # `secondary=posts_tag_table` указывает на вспомогательную таблицу для установления связи


class Tag(Base):
    __tablename__ = 'tags'  # Указываем имя таблицы для модели Post

    # Колонки таблицы
    id: Mapped[int] = mapped_column(primary_key=True)  # Первичный ключ типа Integer
    name: Mapped[str] = mapped_column(String(100))

    # Отношение "многие ко многим" с таблицей Post.
    posts = relationship('Post', back_populates='tags', lazy="select", secondary=posts_tag_table)
    # `secondary=posts_tag_table` указывает на вспомогательную таблицу для установления связи
