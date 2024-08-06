from fastapi import APIRouter, Depends

from app.database import get_session
from app.schemas.posts import PostSchema, CreatePostSchema
from app.services.posts import create_post, get_posts
from app.services.users import get_current_user

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("", response_model=list[PostSchema])
def get_all_posts_view(session=Depends(get_session, use_cache=True)):
    """
    Получение всех постов.

    :param session: Сессия базы данных, полученная с помощью зависимости.
    :return: Список всех постов, представленных в формате PostSchema.
    """
    return get_posts(session)


@router.post("", response_model=PostSchema)
def create_post_view(
    post_data: CreatePostSchema,
    user=Depends(get_current_user),
    session=Depends(get_session, use_cache=True),
):
    """
    Создание нового поста.

    :param post_data: Данные для создания поста, валидированные через CreatePostSchema.
    :param user: Текущий пользователь, полученный с помощью зависимости.
    :param session: Сессия базы данных, полученная с помощью зависимости.
    :return: Созданный пост, представленный в формате PostSchema.
    """
    return create_post(session, post_data, user)
