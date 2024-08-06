from pydantic import BaseModel, Field, EmailStr


class UserBaseSchema(BaseModel):
    """
    Базовая схема данных для пользователя.
    Содержит обязательные поля username и email.
    """

    # Имя пользователя должно быть строкой длиной от 2 до 50 символов
    username: str = Field(..., min_length=2, max_length=50)

    # Email пользователя должен быть валидным email-адресом и не превышать 256 символов
    email: EmailStr = Field(..., max_length=256)


class UserSchema(UserBaseSchema):
    """
    Схема данных для представления существующего пользователя.
    Наследует поля из UserBaseSchema и добавляет поле id.
    """

    id: int  # ID пользователя, тип int


class UserCreateSchema(UserBaseSchema):
    """
    Схема данных для создания нового пользователя.
    Наследует поля из UserBaseSchema и добавляет поле password.
    """

    # Пароль пользователя должен быть строкой длиной от 8 до 50 символов
    password: str = Field(..., min_length=8, max_length=50)


class UserCredentialsSchema(BaseModel):
    # Имя пользователя должно быть строкой длиной от 2 до 50 символов
    username: str = Field(..., min_length=2, max_length=50)
    # Пароль пользователя должен быть строкой длиной от 8 до 50 символов
    password: str = Field(..., min_length=8, max_length=50)


class AccessTokenSchema(BaseModel):
    access_token: str


class RefreshTokenSchema(BaseModel):
    refresh_token: str


class TokenPairSchema(AccessTokenSchema, RefreshTokenSchema):
    pass
