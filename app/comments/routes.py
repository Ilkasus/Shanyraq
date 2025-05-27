from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Comment, Shanyrak, User
from app.comments.schemas import CommentCreate, CommentOut
from app.utils.security import get_current_user
from typing import List

comment_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@comment_router.post("/{shanyrak_id}", response_model=CommentOut)
def create_comment(shanyrak_id: int, comment: CommentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    sh = db.query(Shanyrak).filter_by(id=shanyrak_id).first()
    if not sh:
        raise HTTPException(status_code=404, detail="Shanyrak not found")
    new_comment = Comment(
        content=comment.content,
        user_id=current_user.id,
        shanyrak_id=shanyrak_id
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

@comment_router.get("/{shanyrak_id}", response_model=List[CommentOut])
def get_comments(shanyrak_id: int, db: Session = Depends(get_db)):
    return db.query(Comment).filter_by(shanyrak_id=shanyrak_id).order_by(Comment.created_at.desc()).all()

