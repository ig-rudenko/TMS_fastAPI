from pydantic import BaseModel, Field


class TagSchema(BaseModel):
    name: str = Field(..., max_length=100)


class CreatePostSchema(BaseModel):
    title: str = Field(..., max_length=256)
    content: str
    tags: list[str]


class PostSchema(CreatePostSchema):
    id: int
    user_id: int
    tags: list[TagSchema]
