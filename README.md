# 🛒 College Marketplace

A clean, fast, and modern **Marketplace web application** built with **FastAPI**, using **JWT authentication**, **PostgreSQL** as database, and **ImageKit** for media storage.  
Users can create accounts, post items for sale, manage their listings, upload images, view items on sale, buy items and securely process payments—all inside a lightweight backend.

🚀 **Live Marketplace Demo:** [Try it here](https://college-marketplace-6wry.onrender.com)

---

## ✨ Features

### 🔐 Authentication

- User Registration & Login
- JWT-based authentication
- Password hashing
- Protected routes for user content

### 📦 Marketplace

- Create new listings (title, description, category, price, images)
- Upload item images via **ImageKit**
- View all marketplace posts
- View individual post details
- Manage your own posts (edit / delete)
- User profile page

### 💳 Payments

- Integrated simple payment system  
  (supports mock payments or real gateways depending on configuration)

### 🖼️ UI

- Fully functional HTML templates
- Pages included:
  - `login.html`
  - `register.html`
  - `upload.html`
  - `my_posts.html`
  - `profile.html`
  - `ny_posts.html`

### 🗄️ Database

- Works with **PostgreSQL**
- Configurable via `.env`

### 🐳 Docker Support

Production-ready Dockerfile + docker-compose for:

- FastAPI backend
- PostgreSQL database

---

## 📁 Project Structure

```
app/
├── static/               # HTML templates
│   ├── login.html
│   ├── register.html
│   ├── upload.html
│   ├── my_posts.html
│   ├── profile.html
│   └── ny_posts.html
│
├── __init__.py
├── main.py               # App entrypoint
├── auth.py               # JWT auth logic
├── crud.py               # Database operations
├── database.py           # DB connections
├── images.py             # ImageKit utilities
├── model.py              # SQLAlchemy models
└── schemas.py            # Pydantic schemas

docker-compose.yml
Dockerfile
requirements.txt
README.md
```

---

## ⚙️ Tech Stack

- **FastAPI** – Backend web framework
- **Python**
- **JWT Auth** – Secure token-based login
- **SQLAlchemy** – ORM for database operations
- **PostgreSQL** – Databases
- **ImageKit** – External storage for images
- **Uvicorn** – ASGI server
- **Docker & Docker Compose** – Deployment
- **python-multipart** – File uploads

---

## 🚀 Getting Started

### 1️⃣ Clone the repository

```bash
git clone <repo-url>
cd College-Marketplace
```

### 2️⃣ Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate      # Linux / Mac
.venv\Scripts\activate         # Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Set up environment variables

Set up your environment varialbles in `.env` as in `.env.example`

### 5️⃣ Run the server

```bash
uvicorn app.main:app --reload
```

Visit:  
👉 **http://127.0.0.1:8000**

---

## 🧪 Example Usage

### Register a user

POST `/register`

### Login

POST `/login`  
Returns a JWT token.

### Create a post

POST `/upload`  
Requires:

- Title
- Description
- Price
- Image file
- Auth token

### View all posts

GET `/posts`

---

## 🐳 Run with Docker (Recommended)

### Build & Run with Docker Compose

```bash
docker compose up --build
```

---

## 👤 Author

**Arghya Malakar**  
📧 arghyaapply2016@gmail.com  
🌐 GitHub: https://github.com/hunterarghya
