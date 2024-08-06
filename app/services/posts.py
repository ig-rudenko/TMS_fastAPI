from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models import Post, Tag, User
from app.schemas.posts import CreatePostSchema


def get_posts(session: Session) -> Sequence[Post]:
    """
    Возвращает все посты из базы данных.

    :param session: Объект сессии для взаимодействия с базой данных.
    :return: Список всех постов.
    """
    # `session.scalars(...)` Выполняет запрос и возвращает результаты в виде скаляров (одиночных значений),
    # представляющих записи Post.
    # `selectinload(Post.tags)` используется для выполнения эффективного запроса и загрузки тегов
    # (связанных объектов Tag) вместе с основными записями Post в одном запросе.
    # Это предотвращает проблему "N+1 запросов", когда для каждой записи Post делается отдельный
    # запрос для загрузки связанных Tag.
    return session.scalars(select(Post).options(selectinload(Post.tags))).all()


def create_post(session: Session, post_data: CreatePostSchema, user: User) -> Post:
    """
    Создает новый пост в базе данных.

    :param session: Объект сессии для взаимодействия с базой данных.
    :param post_data: Данные для создания поста, переданные через схему CreatePostSchema.
    :param user: Объект пользователя, который создает пост.
    :return: Созданный объект поста.
    """
    # Получаем или создаем теги, указанные в post_data.tags, без фиксации изменений в базе данных.
    tags = _get_or_create_tags(session, post_data.tags)

    # Создаем объект Post с переданными данными
    post = Post(
        title=post_data.title,
        content=post_data.content,
        user_id=user.id,
    )
    post.tags = tags  # Привязываем теги к посту
    session.add(post)  # Добавляем новый пост в сессию
    session.commit()  # Фиксируем изменения в базе данных

    # Обновляем объект post из базы данных, чтобы получить все его обновленные поля, такие как id
    session.refresh(post)
    return post


def _get_or_create_tags(session: Session, tags: list[str]) -> list[Tag]:
    """
    Находит или создает список тегов без commit.

    :param session: Объект сессии для взаимодействия с базой данных.
    :param tags: Список имен тегов.
    :return: Список объектов Tag.
    """
    model_tags = []  # Список для хранения объектов Tag
    for tag_name in tags:
        # Выполняем запрос для поиска тега по имени (независимо от регистра)
        result = session.execute(select(Tag).where(Tag.name.ilike(tag_name)))
        result.unique()  # Убедиться, что результат уникален (одна запись)

        # Получаем тег из результата запроса, если он существует, иначе None
        tag = result.scalar_one_or_none()
        if tag is None:
            # Если тег не найден, создаем новый объект Tag
            tag = Tag(name=tag_name)

        model_tags.append(tag)  # Добавляем тег в список model_tags

    # Добавляем все теги в сессию
    session.add_all(model_tags)

    # Возвращаем список тегов
    return model_tags
