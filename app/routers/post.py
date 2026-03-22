from typing import Optional
from fastapi import Depends, HTTPException, status, APIRouter
from .. import schema, models
from sqlalchemy.orm import Session
from ..database import get_db
from ..oauth2 import get_current_user
from sqlalchemy import func

router = APIRouter(prefix="/posts", tags=["Posts"])

# Two types to accept request body and validate:
# 1st: Body(...) Accepts input request body and convert it into dict. Returns error if no request body found.

@router.get('/', response_model=list[schema.PostOut])
def get_posts(db: Session = Depends(get_db), current_user:schema.User = Depends(get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    '''posts = db.query(models.Posts).filter(models.Posts.title.contains(search)).limit(limit).offset(skip).all()'''
    posts = db.query(models.Posts, func.count(models.Votes.post_id).label("votes")) \
        .join(models.Votes, models.Posts.id == models.Votes.post_id, isouter=True) \
        .group_by(models.Posts.id) \
        .filter(models.Posts.title.contains(search)).limit(limit).offset(skip) \
        .all()

    result = []

    for post, votes in posts:
        result.append({
            "post": post,
            "votes": votes
        })

    return result

# @app.get('/posts/latest')
# def get_latest_post():
#     return {"latest_post": temp_posts[-1]}

@router.get("/{id}", response_model=schema.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user:schema.User = Depends(get_current_user)):
    post = db.query(models.Posts, func.count(models.Votes.post_id).label("votes")) \
        .join(models.Votes, models.Posts.id == models.Votes.post_id, isouter=True) \
        .group_by(models.Posts.id) \
        .filter(models.Posts.id == id).first()

    # Manual way
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()
    # print(post, id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post not found")
    return post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.Post)
def create_post(post: schema.PostCreate, db: Session = Depends(get_db), current_user: schema.User = Depends(get_current_user)):
    new_post = models.Posts(user_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    # Manual way
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    # created_post = cursor.fetchone()
    # conn.commit()
    return new_post

@router.put("/{id}", response_model=schema.Post, )
def update_post(id: int, updated_post: schema.PostCreate, db: Session = Depends(get_db), current_user:schema.User = Depends(get_current_user)):
    post = db.query(models.Posts).filter(models.Posts.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found for update")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    post.title = updated_post.title
    post.content = updated_post.content
    post.published = updated_post.published

    db.commit()
    db.refresh(post)

    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    #
    # print(updated_post)
    return post

@router.delete("/{id}")
def delete_post(id:int, db: Session = Depends(get_db), current_user:schema.User = Depends(get_current_user)):
    post_query = db.query(models.Posts).filter(models.Posts.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    post_query.delete(synchronize_session=False)
    db.commit()
    # Manual way
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", str(id))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    # print(deleted_post)

    return {"data": f"Item with id {id} deleted"}
