from fastapi import status, Depends, HTTPException, APIRouter
from .. import schema, models, helper
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(prefix="/user", tags=["User"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.User)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    try:
        user.password = helper.hash_password(user.password)
        new_user = models.User(**user.model_dump())
        db.add(new_user)
        # first check the validations and then commit to db.
        db.flush()
        db.refresh(new_user)
        schema.User.model_validate(new_user)
        db.commit()
        return new_user
    except:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

@router.get("/{uid}", status_code=status.HTTP_200_OK, response_model=schema.User)
def get_user(uid: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == uid).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user