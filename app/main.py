# from fastapi import FastAPI, HTTPException, BackgroundTasks, Request, Depends, File, UploadFile, Form
# from fastapi.responses import HTMLResponse
# from fastapi.middleware.cors import CORSMiddleware
# from sqlalchemy.orm import Session
# from fastapi.templating import Jinja2Templates

# from app import schemas, model, crud
# from app.database import get_db, engine, Base
# from app.schemas import Post_item, PostUpdate

# from app.images import imagekit
# from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions

# from sqlalchemy import select

# import shutil
# import os
# import uuid
# import tempfile

# # from app.auth.routes import auth_router, register_router, reset_router, verify_router
# # from app.auth.routes import current_active_user
# from app.auth import router as auth_router, current_active_user



# Base.metadata.create_all(bind=engine)


# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app.include_router(auth_router)  # /auth prefix already in the router

# app.include_router(auth_router, prefix="/auth/jwt", tags=["auth"])
# app.include_router(register_router, prefix="/auth", tags=["auth"])
# app.include_router(reset_router, prefix="/auth", tags=["auth"])
# app.include_router(verify_router, prefix="/auth", tags=["auth"])

# @app.get("/")
# def hello():
#     return {"message": "hello api is running"}

# @app.post("/upload")
# def upload_file(
#     file: UploadFile = File(...),
#     title: str = Form(""),
#     description: str = Form(""),
#     location: str = Form(""),
#     price: int = Form(...),
#     db: Session = Depends(get_db),
#     user = Depends(current_active_user)
# ):
    
#     temp_file_path = None
#     try:
#         # Save UploadFile to a temp file
#         suffix = os.path.splitext(file.filename)[1] or ""
#         with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
#             temp_file_path = tmp.name
#             file.file.seek(0)
#             shutil.copyfileobj(file.file, tmp)

#         # Upload to ImageKit
#         with open(temp_file_path, "rb") as f:
#             upload_result = imagekit.upload_file(
#                 file=f,
#                 file_name=file.filename,
#                 options=UploadFileRequestOptions(
#                     use_unique_file_name=True,
#                     tags=["college-marketplace-backend-upload"]
#                 )
#             )

#         # Check upload result
#         status_code = None
#         # Depending on imagekit python client, response structure may differ.
#         # Try to read response metadata safely:
#         if hasattr(upload_result, "response_metadata"):
#             status_code = getattr(upload_result.response_metadata, "http_status_code", None)
#         # Fallback: some clients return dict-like response
#         if status_code is None:
#             status_code = upload_result.get("response_metadata", {}).get("http_status_code") if isinstance(upload_result, dict) else None

#         if status_code == 200 or upload_result and getattr(upload_result, "url", None):
#             uploaded_url = getattr(upload_result, "url", None) or upload_result.get("url")
#             uploaded_name = getattr(upload_result, "name", None) or upload_result.get("name") or file.filename

#             post = crud.create_post(
#                 db=db,
#                 user_id=user.id,               # ← FIXED (very important)
#                 title=title,
#                 description=description,
#                 price=price,
#                 location=location,
#                 url=uploaded_url,
#                 file_type=file.content_type or "image",
#                 file_name=uploaded_name
#             )
#             # post = crud.create_post(
#             #     db=db,
#             #     title=title,
#             #     description=description,
#             #     price=price,
#             #     location=location,
#             #     url=uploaded_url,
#             #     file_type=file.content_type or "image",
#             #     file_name=uploaded_name
#             # )
#             return post
#         else:
#             raise HTTPException(status_code=500, detail="Image upload failed")

#     except HTTPException:
#         raise
#     except Exception as e:
#         # log e
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         # cleanup
#         if temp_file_path and os.path.exists(temp_file_path):
#             os.unlink(temp_file_path)
#         # UploadFile's file is a SpooledTemporaryFile - close it
#         try:
#             file.file.close()
#         except Exception:
#             pass
#     # post = crud.create_post(db, title, description, price, location, url="dummy url", file_type="photo", file_name="dummy name")

#     # return {
#     #     "title": post.title,
#     #     "description": post.description,
#     #     "price": post.price,
#     #     "location": post.location,
#     #     "url": post.url,
#     #     "file_type": post.file_type,
#     #     "file_name": post.file_name
#     # }

# @app.get("/feed")
# def get_feed(db: Session = Depends(get_db)):
#     posts = crud.get_feed(db)
#     if not posts:
#         raise HTTPException(status_code=404, detail= "post not found")
#     return posts


# @app.delete("/post/{post_id}")
# def delete_post(post_id: str, db: Session = Depends(get_db)):
#     post_uuid = uuid.UUID(post_id)

#     result = crud.delete_post(db, post_uuid)

#     if not result:
#         raise HTTPException(status_code=404, detail="Post not found")
    

#     return {"message": "Post deleted successfully"}


# @app.patch("/post/{post_id}")
# def edit_post(post_id: str, data: PostUpdate, db: Session = Depends(get_db)):
#     post_uuid = uuid.UUID(post_id)

#     updated_post = crud.update_post(db, post_uuid, data)

#     if not updated_post:
#         raise HTTPException(status_code=404, detail="Post not found")

#     return updated_post


from fastapi import FastAPI, HTTPException, Depends, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import shutil
import os
import uuid
import tempfile

from app.database import get_db, engine, Base
from app import crud
from app.schemas import PostUpdate
from app.auth import router as auth_router, current_active_user
from app.images import imagekit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions


# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# ---- CORS ----
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- AUTH ROUTER ----
app.include_router(auth_router)    # → gives /auth/register, /auth/login, /auth/jwt/login


# -----------------------------------------------------------
# ROOT
# -----------------------------------------------------------
@app.get("/")
def home():
    return {"message": "API Running OK"}


# -----------------------------------------------------------
# UPLOAD POST (PROTECTED)
# -----------------------------------------------------------
@app.post("/upload")
def upload_file(
    file: UploadFile = File(...),
    title: str = Form(""),
    description: str = Form(""),
    location: str = Form(""),
    price: int = Form(...),
    db: Session = Depends(get_db),
    user = Depends(current_active_user),
):
    temp_file_path = None
    try:
        # Save to temp file
        suffix = os.path.splitext(file.filename)[1] or ""
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            temp_file_path = tmp.name
            file.file.seek(0)
            shutil.copyfileobj(file.file, tmp)

        # Upload to ImageKit
        with open(temp_file_path, "rb") as f:
            upload_result = imagekit.upload_file(
                file=f,
                file_name=file.filename,
                options=UploadFileRequestOptions(
                    use_unique_file_name=True,
                    tags=["college-marketplace-backend-upload"],
                ),
            )

        status_code = (
            getattr(upload_result.response_metadata, "http_status_code", None)
            if hasattr(upload_result, "response_metadata")
            else None
        )

        if status_code == 200:
            uploaded_url = upload_result.url
            uploaded_name = upload_result.name

            post = crud.create_post(
                db=db,
                user_id=user.id,
                title=title,
                description=description,
                price=price,
                location=location,
                url=uploaded_url,
                file_type=file.content_type or "image",
                file_name=uploaded_name,
            )
            return post

        raise HTTPException(status_code=500, detail="Image upload failed")

    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        try:
            file.file.close()
        except:
            pass


# -----------------------------------------------------------
# FEED (PROTECTED)
# -----------------------------------------------------------
@app.get("/feed")
def get_feed(
    db: Session = Depends(get_db),
    user = Depends(current_active_user),
):
    posts = crud.get_feed(db)
    return posts


# -----------------------------------------------------------
# DELETE POST (PROTECTED + OWNER ONLY)
# -----------------------------------------------------------
@app.delete("/post/{post_id}")
def delete_post(
    post_id: str,
    db: Session = Depends(get_db),
    user = Depends(current_active_user),
):
    post_uuid = uuid.UUID(post_id)
    post = db.query(crud.model.PostItems).filter_by(id=post_uuid).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # AUTHORIZATION: Only owner can delete
    if post.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    result = crud.delete_post(db, post_uuid)
    if not result:
        raise HTTPException(status_code=404, detail="Post not found")

    return {"message": "Post deleted successfully"}


# -----------------------------------------------------------
# EDIT POST (PATCH) (PROTECTED + OWNER ONLY)
# -----------------------------------------------------------
@app.patch("/post/{post_id}")
def edit_post(
    post_id: str,
    data: PostUpdate,
    db: Session = Depends(get_db),
    user = Depends(current_active_user),
):
    post_uuid = uuid.UUID(post_id)
    post = db.query(crud.model.PostItems).filter_by(id=post_uuid).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # AUTHORIZATION: Only owner can edit
    if post.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    updated_post = crud.update_post(db, post_uuid, data)
    return updated_post
