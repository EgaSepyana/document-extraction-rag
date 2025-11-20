# ⚡ React + Vite + Tailwind CSS Frontend

Project ini adalah **frontend modern** yang dibangun menggunakan **React**, **Vite**, dan **Tailwind CSS**.  
Tujuannya buat bikin UI yang cepat, ringan, dan gampang dikembangkan — cocok buat dashboard, landing page, atau aplikasi modern.

---

## 🧠 Tech Stack

- ⚛️ **React 18+** — library utama untuk UI  
- ⚡ **Vite** — super cepat buat dev & build  
- 🎨 **Tailwind CSS** — styling simple dan fleksibel

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository
```bash
git clone <git-src>
cd document-extraction-rag
git checkout fe-app
```

# 2️⃣ Install Dependencies

```bash
npm install
# atau
yarn install
# atau
pnpm install
```

# 3️⃣ Jalankan Development Server
```bash
npm run dev
# atau
yarn dev
```


# 🚀 FastAPI + MongoDB REST API Backend

Project ini adalah RESTful API berbasis **Python** menggunakan **FastAPI** dan **MongoDB**.  
Didesain untuk performa tinggi, asynchronous, dan mudah dikembangkan untuk berbagai use case backend modern.

---

## 🧠 Tech Stack

- 🐍 **Python 3.10+**
- ⚡ **FastAPI** — web framework modern & cepat
- 🍃 **MongoDB** — database NoSQL untuk penyimpanan data
- 🔁 **Pymongo** — driver MongoDB
- 🧩 **Pydantic** — validasi & schema data
- 🌱 **Uvicorn** — ASGI server
- 🔐 **python-dotenv** — environment loader


## ⚙️ Installation & Setup
# 1️⃣ Clone repository

```bash
git clone <git-src>
cd document-extraction-rag
git checkout be-svc
```

# 2️⃣ Buat virtual environment
```bash
python -m venv venv
source venv/bin/activate       # Mac / Linux
venv\Scripts\activate          # Windows
```

# 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

# 4️⃣ Buat file .env

```bash
cp .env.example .env
```

# 🧾 .env.example

```bash
# API
LLM_API_KEY=
LLM_BASE_URL=
EMBEDDING_BASE_URL=

# DB
VECTOR_DB=  # chroma or faiss

# AI
MODEL_NAME=
EMBEDING_MODEL=
EMBEDDING_SIZE=

ACTIVE_ROUTERS={}

# # Deployment
PROJECT_SERVICE_PORT=
SVC_MANAGEMENT_NAME=
REGISTRY=
PROJECT_NAME=
SERVER_SERVICE=
SERVER_DEPLOY_USER=
SERVER_DEPLOY_PASS=

BASE_POSTGRESQL_URL=

POSTGRESQL_TABLE_DOCUMENT=
```

# ▶️ Jalankan Server
```bash
uvicorn main:app --reload
```

# ▶️ Cara Lain Untuk Jalankan Server
```bash
python main.py
```

# 🧠 API Docs
FastAPI auto-generate dokumentasi interaktif:
Swagger UI → http://localhost:8000/docs 
OR
Swagger UI → http://localhost:{service_port}/docs