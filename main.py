from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User, Post
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic model for input/output
class UserCreate(BaseModel):
    name: str
    email: str

class UserOut(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True

class PostCreate(BaseModel):
    title: str
    content: str
    user_id: int

class PostOut(BaseModel):
    id: int
    title: str
    content: str
    user_id: int

    class Config:
        orm_mode = True

# API endpoints
# Create a new user
@app.post("/users/", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Get all users
@app.get("/users/", response_model=list[UserOut])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

# Get a specific user
@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Update a user
@app.put("/users/{user_id}", response_model=UserOut)
def update_user(user_id: int, updated: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.name = updated.name
    user.email = updated.email
    db.commit()
    db.refresh(user)
    return user

# Delete a user
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"msg": "User deleted"}

# Create a new post
@app.post("/posts/", response_model=PostOut)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    new_post = Post(title=post.title, content=post.content, user_id=post.user_id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# Get all posts
@app.get("/posts/", response_model=List[PostOut])
def get_posts(db: Session = Depends(get_db)):
    return db.query(Post).all()

# Get a specific post
@app.get("/posts/", response_model=List[PostOut])
def get_posts(db: Session = Depends(get_db)):
    return db.query(Post).all()

# Update a post
@app.put("/posts/{post_id}", response_model=PostOut)
def update_post(post_id: int, updated: PostCreate, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    post.title = updated.title
    post.content = updated.content
    post.user_id = updated.user_id
    db.commit()
    db.refresh(post)
    return post

# Delete a post
@app.delete("/posts/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    db.delete(post)
    db.commit()
    return {"msg": "Post deleted"}

# Get all posts for a specific user
@app.get("/users/{user_id}/posts", response_model=List[PostOut])
def get_user_posts(user_id: int, db: Session = Depends(get_db)):
    return db.query(Post).filter(Post.user_id == user_id).all()
