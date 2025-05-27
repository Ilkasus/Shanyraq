from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app.models import Shanyrak, User
from app.shanyraks.schemas import ShanyrakCreate, ShanyrakOut, ShanyrakUpdate
from app.utils.security import get_current_user

shanyrak_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@shanyrak_router.post("/", response_model=ShanyrakOut)
def create_shanyrak(shanyrak: ShanyrakCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_shanyrak = Shanyrak(**shanyrak.dict(), owner_id=current_user.id)
    db.add(new_shanyrak)
    db.commit()
    db.refresh(new_shanyrak)
    return new_shanyrak

@shanyrak_router.get("/", response_model=List[ShanyrakOut])
def get_all_shanyraks(db: Session = Depends(get_db)):
    return db.query(Shanyrak).order_by(Shanyrak.created_at.desc()).all()

@shanyrak_router.get("/{shanyrak_id}", response_model=ShanyrakOut)
def get_one_shanyrak(shanyrak_id: int, db: Session = Depends(get_db)):
    sh = db.query(Shanyrak).filter_by(id=shanyrak_id).first()
    if not sh:
        raise HTTPException(status_code=404, detail="Not found")
    return sh

@shanyrak_router.put("/{shanyrak_id}", response_model=ShanyrakOut)
def update_shanyrak(shanyrak_id: int, data: ShanyrakUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    sh = db.query(Shanyrak).filter_by(id=shanyrak_id).first()
    if not sh or sh.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Permission denied")
    for key, value in data.dict(exclude_unset=True).items():
        setattr(sh, key, value)
    db.commit()
    db.refresh(sh)
    return sh

@shanyrak_router.delete("/{shanyrak_id}")
def delete_shanyrak(shanyrak_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    sh = db.query(Shanyrak).filter_by(id=shanyrak_id).first()
    if not sh or sh.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Permission denied")
    db.delete(sh)
    db.commit()
    return {"detail": "Deleted"}
