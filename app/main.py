from fastapi import FastAPI, HTTPException, Depends, File, UploadFile, Form, Request
from fastapi.templating import Jinja2Templates
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

from urllib.parse import quote
from app.auth import get_current_user
# from app.auth import razorpayx
from app.model import PostItems, User

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse

from dotenv import load_dotenv
import razorpay


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(auth_router)    



@app.get("/")
def home():
    return FileResponse("app/static/login.html")


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


@app.get("/feed")
def get_feed(
    db: Session = Depends(get_db),
    user = Depends(current_active_user),
):
    posts = crud.get_feed(db)
    return posts


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





# ...............................
# ...............................
# ...............................
# ...............................
# ...............................
# ...............................
# ...............................
# ...............................

# UPI
# PAYMENT
# USING
# URL
# ...............................
# ...............................
# ...............................
# ...............................
# ...............................
# ...............................
# ...............................
# ...............................







# @app.get("/generate_upi_link/{post_id}")
# def generate_upi_link(
#     post_id: str,
#     db: Session = Depends(get_db),
#     current_user = Depends(get_current_user)
# ):
#     post_uuid = uuid.UUID(post_id)

#     post = db.query(PostItems).filter(
#         PostItems.id == post_uuid,
#         PostItems.status == "available"
#     ).first()

#     if not post:
#         raise HTTPException(status_code=404, detail="Post not found or not available")

#     seller = post.user                    
#     buyer = current_user                  

#     # upi_url = (
#     #     f"upi://pay?"
#     #     f"pa={seller.upi_id}&"
#     #     f"pn={quote(seller.name)}&"
#     #     f"tn=Payment+for+{quote(post.title)}&"
#     #     f"am={post.price}&"
#     #     f"cu=INR"
#     # )

#     upi_url = (
#         "upi://pay?"
#         f"pa={quote(seller.upi_id)}&"
#         f"pn={quote(seller.name)}&"
#         f"am={post.price}&"
#         f"tn={quote('Payment for ' + post.title)}&"
#         f"cu=INR"
#     )

#     return {"upi_link": upi_url}



# @app.post("/confirm_payment/{post_id}")
# def confirm_payment(
#     post_id: str,
#     db: Session = Depends(get_db),
#     current_user = Depends(get_current_user)
# ):
#     post_uuid = uuid.UUID(post_id)

#     post = db.query(PostItems).filter(PostItems.id == post_uuid).first()

#     if not post:
#         raise HTTPException(status_code=404, detail="Post not found")

#     if post.status == "sold":
#         raise HTTPException(status_code=400, detail="Already sold")

#     post.status = "sold"
#     db.commit()
#     db.refresh(post)

#     return {"message": "Payment confirmed", "post_id": post_id}










# ...............................
# ...............................
# ...............................
# ...............................
# ...............................
# ...............................
# ...............................
# ...............................

# RAZORPAY
# PAYMENT
# GATEWAY
# INTEGRATION
# ...............................
# ...............................
# ...............................
# ...............................
# ...............................
# ...............................
# ...............................
# ...............................


load_dotenv()

RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")

razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

templates = Jinja2Templates(directory="app/static")


@app.get("/create_order/{post_id}")
def create_order(
    post_id: str,
    db: Session = Depends(get_db),
    user=Depends(current_active_user)
):
    post_uuid = uuid.UUID(post_id)

    post = db.query(PostItems).filter(
        PostItems.id == post_uuid, 
        PostItems.status == "available"
    ).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found or unavailable")

    amount_in_paisa = int(post.price * 100)

    order = razorpay_client.order.create({
        "amount": amount_in_paisa,
        "currency": "INR",
        "payment_capture": 1
    })

    return {
        "order_id": order["id"],
        "amount": amount_in_paisa,
        "currency": "INR",
        "key": RAZORPAY_KEY_ID,
        "post_id": post_id,
        "title": post.title
    }


@app.post("/verify_payment")
async def verify_payment(
    request: Request,
    db: Session = Depends(get_db),
    user=Depends(current_active_user)
):
    body = await request.json()

    order_id = body.get("razorpay_order_id")
    payment_id = body.get("razorpay_payment_id")
    signature = body.get("razorpay_signature")
    post_id = body.get("post_id")

    if not (order_id and payment_id and signature and post_id):
        raise HTTPException(status_code=400, detail="Missing payment details")

    try:
        razorpay_client.utility.verify_payment_signature({
            "razorpay_order_id": order_id,
            "razorpay_payment_id": payment_id,
            "razorpay_signature": signature
        })
    except:
        return {"status": "failed", "message": "Signature verification failed"}

    post_uuid = uuid.UUID(post_id)

    post = db.query(PostItems).filter_by(id=post_uuid).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    post.status = "sold"
    db.commit()


    # # --------------------------(PAYOUT) --------------------------
    # # --------------------------(PAYOUT) --------------------------
    # # --------------------------(PAYOUT) --------------------------
    # # --------------------------(PAYOUT) --------------------------
    # seller = db.query(User).filter(User.id == post.user_id).first()

    # if not seller.fund_account_id:
    #     raise HTTPException(status_code=500, detail="Seller payout account missing")

    # payout_data = {
    #     "account_number": os.getenv("RAZORPAYX_ACCOUNT_NUMBER"),
    #     "fund_account_id": seller.fund_account_id,
    #     "amount": int(post.price * 100),  # Razorpay takes amount in paise
    #     "currency": "INR",
    #     "mode": "UPI",
    #     "purpose": "payout",
    #     "queue_if_low_balance": True,
    #     "reference_id": str(post.id)
    # }

    # payout = razorpayx.payout.create(payout_data)
    # # -------------------------------------------------------------------
    # # -------------------------------------------------------------------
    # # -------------------------------------------------------------------
    # # -------------------------------------------------------------------
    # # -------------------------------------------------------------------

    return {"status": "success", "message": "Payment verified", "post_id": post_id}
