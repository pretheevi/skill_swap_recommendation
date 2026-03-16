# SkillSwap Recommendation Service

A lightweight recommendation microservice used by SkillSwap to generate personalized skill recommendations for users.

The service is built with **FastAPI** and uses an **implicit ALS matrix-factorization model** trained on user interactions (likes, comments, follows). It exposes a simple REST endpoint that returns recommended skill IDs for a given user.

---

## 💡 What This Service Does

- Trains a collaborative filtering model using user behavior data from the SkillSwap database (likes/comments/follows).
- Produces ranked recommendations of skills for a given user.
- Returns trending skill recommendations when a user has no interaction history.
- Supports hot-reloading of the model via a `/reload-model` endpoint.

---

## 🧠 Architecture

### Core Components

- `app.py` - FastAPI application entrypoint, lifecycle management, and API routes.
- `ml.py` - Model training and inference logic.
- `generateData.py` - Synthetic dataset generator (useful for local testing).
- `requirements.txt` - Python dependencies.

### Data Source

Reads interaction data from the same SQLite/Turso database used by SkillSwap, using `libsql_experimental`.

Interaction sources:

- `Skill_Likes` (weight = 1)
- `Comment` (weight = 2)
- `user_follows` + skill ownership (weight = 1.5)

These are combined into a single sparse interaction matrix for training.

---

## 🚀 Quick Start (Local)

### Prerequisites

- Python 3.11+
- `pip`
- Access to the SkillSwap database (SQLite/Turso) and environment variables configured.

### Install

```bash
cd recommendation_service
pip install -r requirements.txt
```

### Run

```bash
python app.py
```

The service will be available at:

- HTTP: `http://localhost:8001`
- Recommendation endpoint: `GET /recommend/{user_id}`

---

## 📡 API Endpoints

### `GET /recommend/{user_id}`

Returns `n` recommended skill IDs for a user.

**Query parameters**:

- `n` (optional, default 10) - number of recommendations

**Example**:

```bash
curl "http://localhost:8001/recommend/123?n=15"
```

**Response**:

```json
[
  {"skill_id": "42", "score": 0.2345},
  {"skill_id": "17", "score": 0.2130},
  ...
]
```

### `POST /reload-model`

Reloads and retrains the recommendation model from the database.

**Example**:

```bash
curl -X POST http://localhost:8001/reload-model
```

---

## 🧠 Model Details

- Uses **Implicit ALS** (`implicit` library) for collaborative filtering.
- Trained on a sparse user×skill interaction matrix.
- New users (cold start) receive trending skills based on most-liked items.
- Model is cached in-memory for fast inference.

### Training Pipeline (in `ml.py`)

1. Query interaction data with a SQL union of likes/comments/follow-based implicit signals.
2. Build index mappings for users/skills.
3. Construct a sparse CSR matrix.
4. Train `implicit.als.AlternatingLeastSquares`.

---

## 🧪 Data Generation (Optional)

`generateData.py` is a helper script for populating the Turso/SQLite database with fake users, skills, and interactions.

It uses `Faker` and Unsplash to generate:

- mock user profiles
- mock skill posts (categorized content)
- random likes/comments/follows

Run it with:

```bash
python generateData.py
```

> ⚠️ Only use this script for local/dev experiments; it will insert data into your configured database.

---

## 🔧 Environment Variables

Create a `.env` file (or set these in your deployment environment):

```env
TURSO_URL=https://<your-turso-instance>.turso.tech
TURSO_TOKEN=<your-turso-token>

# Optional: if using Unsplash for data generation
UNSPLASH_ACCESS_KEY=<your-unsplash-key>
```

---

## 🧩 Deployment Notes

- The service is designed to run as a standalone microservice (FastAPI + Uvicorn).
- It is lightweight and can be deployed with Docker / Cloud Run / serverless.
- Use a process manager (Gunicorn/UVicorn, Docker, or similar) and provision enough memory for model training.

---

## 📦 Python Dependencies

Managed via `requirements.txt`:

- `fastapi` / `uvicorn` — web server
- `implicit` — ALS recommendation engine
- `libsql-experimental` — Turso/SQLite access
- `scipy` / `numpy` — matrix operations
- `python-dotenv` — env config
- `requests`, `faker`, `bcrypt` — data generation & utilities

---

## ✅ Notes & Best Practices

- Model training happens on startup and can be reloaded via `/reload-model`.
- For production, schedule periodic retraining (cron, workflow) after interaction data changes.
- Monitor latency and memory usage; ALS training is CPU/memory intensive.

---

_This service is intended to be consumed by the SkillSwap frontend and is not user-facing._
