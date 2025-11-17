from sqlalchemy.orm import Session
from app import model
from datetime import datetime

from app.images import imagekit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions

from fastapi import HTTPException


def create_post(db: Session, title, description, price, location, url, file_type, file_name):

    # temp_file_path = None

    # try:
    #     with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
    #         temp_file_path = temp_file.name
    #         shutil.copyfileobj(file.file, temp_file)
        
    #     upload_result = imagekit.upload_file(
    #         file= open(temp_file_path, "rb"),
    #         file_name= file.filename,
    #         options= UploadFileRequestOptions(
    #             use_unique_file_name=True,
    #             tags=["college-marketplace-backend-upload"]
    #         )
    #     )

    #     if upload_result.response_metadata.http_status_code == 200:


    #         post = model.PostItems(
    #             title = title,
    #             description = description,
    #             price = price,
    #             location = location,
    #             url = upload_result.url,
    #             file_type = "image",
    #             file_name = upload_result.name
    #         )

    #         db.add(post)
    #         db.commit()
    #         db.refresh(post)
    #         return post
        
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))
    # finally:
    #     if temp_file_path and os.path.exists(temp_file_path):
    #         os.unlink(temp_file_path)
    #     file.close()


        
    post = model.PostItems(
        title = title,
        description = description,
        price = price,
        location = location,
        url = url,
        file_type = file_type,
        file_name = file_name
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