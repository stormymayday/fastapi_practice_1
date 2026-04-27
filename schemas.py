from pydantic import BaseModel, Field, ConfigDict

class PostBase(BaseModel):
    title: str = Field(max_length=100)
    content: str
    published: bool = False

class PostCreate(PostBase):
    pass

class PostRead(PostBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
