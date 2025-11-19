from sqlalchemy.orm import Session
from app import model
from datetime import datetime

from app.images import imagekit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions

from fastapi import HTTPException
import uuid


# def create_post(db: Session, user_id:str, title, description, price, location, url, file_type, file_name):
        
    
#     post = model.PostItem(
#         id=uuid.uuid4(),
#         user_id=user_id,               # ← FIXED
#         title=title,
#         description=description,
#         price=price,
#         location=location,
#         url=url,
#         file_type=file_type,
#         file_name=file_name
#     )
#     try:
#         db.add(post)
#         db.commit()
#         db.refresh(post)
#         return post
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail=str(e))

def create_post(
    db: Session,
    user_id: str,
    title: str,
    description: str,
    price: int,
    location: str,
    url: str,
    file_type: str,
    file_name: str
):
    post = model.PostItems(
        id=uuid.uuid4(),
        user_id=user_id,
        title=title,
        description=description,
        price=price,
        location=location,
        url=url,
        file_type=file_type,
        file_name=file_name
    )
    try:
        db.add(post)
        db.commit()
        db.refresh(post)
        return post
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

def get_feed(db: Session):
    return(
        db.query(model.PostItems).filter(model.PostItems.status=="available").all()
    )

def delete_post(db: Session, post_uuid):
    post = db.query(model.PostItems).filter(model.PostItems.id == post_uuid).first()

    if not post:
        return None

    # Delete file from ImageKit
    try:
        # file_name MUST be the fileId saved during upload
        imagekit.delete_file(file_id=post.file_name)
    except Exception:
        pass  # even if file delete fails, delete post anyway

    # Delete post from database
    try:
        db.delete(post)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))



def update_post(db: Session, post_id, data):
    post = db.query(model.PostItems).filter(model.PostItems.id == post_id).first()

    if not post:
        return None
    
    # Update only provided fields
    if data.title is not None:
        post.title = data.title

    if data.description is not None:
        post.description = data.description

    if data.price is not None:
        post.price = data.price

    if data.location is not None:
        post.location = data.location

    try:
        db.commit()
        db.refresh(post)
        return post
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
