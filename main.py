from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, sessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class PostBase(BaseModel):
    title: str
    content: str
    user_id: int  
    
class UserBase(BaseModel):
    username : str

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/posts/{post_id}", status_code=status.HTTP_200_OK)
async def read_post(post_id: int, db: db_dependency):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found !")
    return post

@app.get("/posts/", status_code=status.HTTP_200_OK)
async def read_all_posts(db: db_dependency):
    posts = db.query(models.Post).all()
    if posts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="List of Posts not found !")
    return posts


@app.post("/posts/", status_code=status.HTTP_201_CREATED)
async def create_post(post: PostBase, db: db_dependency):
    db_post = models.Post(**post.dict())
    db.add(db_post)
    db.commit()
    
@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id : int, db: db_dependency):
     post_to_delete = db.query(models.Post).filter(models.Post.id == post_id).first()
     if post_to_delete is None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post to delete not found !")
     db.delete(post_to_delete)
     db.commit()
     
@app.put("/posts/{post_id}", status_code=status.HTTP_200_OK)
async def update_post(post_id:int, post_to_update: PostBase, db: db_dependency):
    checked_post_by_id = db.query(models.Post).filter(models.Post.id == post_id).first()
    if checked_post_by_id is None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post to update not found !")
   
    checked_post_by_id.title = post_to_update.title
    checked_post_by_id.content = post_to_update.content
    db.add(checked_post_by_id)
    db.commit()
    db.refresh(checked_post_by_id)
        
    return checked_post_by_id   


@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    
    
@app.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def read_user(user_id: int, db: db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found !")
    return user

@app.get("/users/", status_code=status.HTTP_200_OK)
async def read_all_users(db: db_dependency):
    users = db.query(models.User).all()
    if users is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="List of users not found !")
    return users

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id : int, db: db_dependency):
     user_to_delete = db.query(models.User).filter(models.User.id == user_id).first()
     if user_to_delete is None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User to delete not found !")
     db.delete(user_to_delete)
     db.commit()
     

@app.put("/users/{user_id}", status_code=status.HTTP_200_OK)
async def user(user_id:int, user_to_update: UserBase, db: db_dependency):
    checked_user_by_id = db.query(models.User).filter(models.User.id == user_id).first()
    if checked_user_by_id is None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User to update not found !")
   
    checked_user_by_id.username = user_to_update.username

    db.add(checked_user_by_id)
    db.commit()
    db.refresh(checked_user_by_id)
        
    return checked_user_by_id 
     
