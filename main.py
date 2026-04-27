from posix import stat
from fastapi import FastAPI, HTTPException, Request, Depends, status

from schemas import PostCreate, PostRead
from typing import Annotated

from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db, Base, engine
from models import Post

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    return {
        "message": "service is running"
    }

@app.post("/posts", response_model=PostRead, status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate, db: Annotated[Session, Depends(get_db)]):
    new_post = Post(
        title = post.title,
        content = post.content,
        published = post.published,
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get("/posts/{post_id}", response_model=PostRead, status_code=status.HTTP_200_OK)
def get_post(post_id: int, db: Annotated[Session, Depends(get_db)]):
    post = db.execute(select(Post).where(Post.id == post_id)).scalar_one_or_none()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="post not found"
        )
    return post
    

@app.get("/posts", response_model=list[PostRead], status_code=status.HTTP_200_OK)
def get_posts(db: Annotated[Session, Depends(get_db)]):
    return db.execute(select(Post)).scalars().all()

@app.delete("/posts/{post_id}", response_model=PostRead, status_code=status.HTTP_200_OK)
def delete_post(post_id: int, db: Annotated[Session, Depends(get_db)]):
    post = db.execute(select(Post).where(Post.id == post_id)).scalars().first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="post not found"
        )
    db.delete(post)
    db.commit()
    return {
        "message": "post deleted",
        "post": post,
    }