from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from .. import models, oauth2, database, schema
from ..database import get_db

router = APIRouter(
    prefix="/vote",
    tags=["vote"],
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_vote(vote: schema.Vote, db: Session = Depends(database.get_db), current_user: schema.User = Depends(oauth2.get_current_user)):
    post = db.query(models.Posts).filter(models.Posts.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist")
    vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id, models.Votes.user_id == current_user.id)
    vote_found = vote_query.first()
    if vote_found:
        if vote.dir == 1:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Vote already exists")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"data": "vote deleted successfully"}
    else:
        if vote.dir == 0:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Vote does not exist")
        new_vote = models.Votes(user_id = current_user.id, post_id = vote.post_id)
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        return {"data": "vote created successfully"}

@router.get("/{id}", status_code=status.HTTP_200_OK)
def get_vote(id: str, db: Session = Depends(get_db), current_user: schema.User = Depends(oauth2.get_current_user)):
    post = db.query(models.Posts).filter(models.Posts.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist")
    count = db.query(models.Votes).filter(models.Votes.post_id == id).count()
    return {"post_id": id, "count": count}