from fastapi import FastAPI, HTTPException, BackgroundTasks, Request, Depends, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates

from app import schemas, model, crud
from app.database import get_db, engine, Base

from app.images import imagekit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions

from sqlalchemy import select

import shutil
import os
import uuid
import tempfile



Base.metadata.create_all(bind=engine)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def hello():
    return {"message": "hello api is running"}

@app.post("/upload")
def upload_file(
    file: UploadFile = File(...),
    title: str = Form(""),
    description: str = Form(""),
    location: str = Form(""),
    price: int = Form(...),
    db: Session = Depends(get_db),
):
    
    temp_file_path = None
    try:
        # Save UploadFile to a temp file
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
                    tags=["college-marketplace-backend-upload"]
                )
            )

        # Check upload result
        status_code = None
        # Depending on imagekit python client, response structure may differ.
        # Try to read response metadata safely:
        if hasattr(upload_result, "response_metadata"):
            status_code = getattr(upload_result.response_metadata, "http_status_code", None)
        # Fallback: some clients return dict-like response
        if status_code is None:
            status_code = upload_result.get("response_metadata", {}).get("http_status_code") if isinstance(upload_result, dict) else None

        if status_code == 200 or upload_result and getattr(upload_result, "url", None):
            uploaded_url = getattr(upload_result, "url", None) or upload_result.get("url")
            uploaded_name = getattr(upload_result, "name", None) or upload_result.get("name") or file.filename

            post = crud.create_post(
                db=db,
                title=title,
                description=description,
                price=price,
                location=location,
                url=uploaded_url,
                file_type=file.content_type or "image",
                file_name=uploaded_name
            )
            return post
        else:
            raise HTTPException(status_code=500, detail="Image upload failed")

    except HTTPException:
        raise
    except Exception as e:
        # log e
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # cleanup
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        # UploadFile's file is a SpooledTemporaryFile - close it
        try:
            file.file.close()
        except Exception:
            pass
    # post = crud.create_post(db, title, description, price, location, url="dummy url", file_type="photo", file_name="dummy name")

    # return {
    #     "title": post.title,
    #     "description": post.description,
    #     "price": post.price,
    #     "location": post.location,
    #     "url": post.url,
    #     "file_type": post.file_type,
    #     "file_name": post.file_name
    # }

@app.get("/feed")
def get_feed(db: Session = Depends(get_db)):
    posts = crud.get_feed(db)
    if not posts:
        raise HTTPException(status_code=404, detail= "post not found")
    return posts
