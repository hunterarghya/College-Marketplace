# 🛒 College Marketplace

A **Marketplace web application** built with **FastAPI**, using **JWT authentication**, **PostgreSQL** as database, and **ImageKit** for media storage.  
Users can create accounts, post items for sale, manage their listings, upload images, view items on sale, buy items and securely process payments.

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

## 💳 Payments (Razorpay Integration)

- Integration with **Razorpay Payment Gateway**
- Backend Razorpay order creation
- Secure signature verification
- Payment status update & redirection

### 🖼️ UI

- Fully functional HTML templates

### 🗄️ Database

- Works with **PostgreSQL**
- Configurable via `.env`

### 🐳 Docker Support

Production-ready Dockerfile + docker-compose for:

- FastAPI backend
- PostgreSQL database

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
- **Razorpay** – Payments

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

Set up your environment varialbles in `.env` as in `env_example.txt`

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
