from fastapi import APIRouter, HTTPException, Depends, status
from typing import Annotated
from schemas import PostCreate, PostRead
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import get_db
from models import Post

router = APIRouter()

@router.get("", response_model=list[PostRead], status_code=status.HTTP_200_OK)
def get_posts(db: Annotated[Session, Depends(get_db)]):
    return db.execute(select(Post)).scalars().all()

@router.post("", response_model=PostRead, status_code=status.HTTP_201_CREATED)
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

@router.get("/{post_id}", response_model=PostRead, status_code=status.HTTP_200_OK)
def get_post(post_id: int, db: Annotated[Session, Depends(get_db)]):
    post = db.execute(select(Post).where(Post.id == post_id)).scalar_one_or_none()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="post not found"
        )
    return post

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Annotated[Session, Depends(get_db)]):
    post = db.execute(select(Post).where(Post.id == post_id)).scalars().first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="post not found"
        )
    db.delete(post)
    db.commit()

@router.patch("/{post_id}", response_model=PostRead, status_code=status.HTTP_200_OK)
def update_post(post_id: int, updated_post: PostCreate, db: Annotated[Session, Depends(get_db)]):
    post = db.execute(select(Post).where(Post.id == post_id)).scalar_one_or_none()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="post not found"
        )
    post.title = updated_post.title
    post.content = updated_post.content
    post.published = updated_post.published
    db.commit()
    db.refresh(post)
    return post