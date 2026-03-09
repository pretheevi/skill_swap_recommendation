from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
import uvicorn
from ml import load_model, recommend

@asynccontextmanager
async def lifespan(app: FastAPI):
    await load_model()
    
    scheduler = AsyncIOScheduler()
    scheduler.add_job(load_model, 'interval', minutes=2)
    scheduler.start()
    
    yield
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)

@app.get("/recommend/{user_id}")
async def get_recommendations(user_id: str, n: int = 10):
    return await recommend(user_id, n)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8001, reload=True)