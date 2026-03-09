from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from ml import load_model, recommend

@asynccontextmanager
async def lifespan(app: FastAPI):
    await load_model()
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/reload-model")
async def reload_model():
    await load_model()
    return {"status": "reloaded"}

@app.get("/recommend/{user_id}")
async def get_recommendations(user_id: str, n: int = 10):
    return await recommend(user_id, n)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8001)