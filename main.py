from fastapi import FastAPI
import redis
import os

app = FastAPI()

# Connect to Redis
import redis
import os

redis_url = os.getenv("REDIS_URL")

r = redis.from_url(
    redis_url,
    decode_responses=True
)

@app.get("/")
def home():
    return {"message": "Docker Compose API"}

@app.post("/hit/{key}")
def hit(key: str):
    count = r.incr(key)
    return {
        "key": key,
        "count": count
    }

@app.get("/count/{key}")
def count(key: str):
    value = r.get(key)
    return {
        "key": key,
        "count": int(value) if value else 0
    }

@app.get("/healthz")
def health():
    try:
        r.ping()
        return {
            "status": "ok",
            "redis": "up"
        }
    except:
        return {
            "status": "error",
            "redis": "down"
        }