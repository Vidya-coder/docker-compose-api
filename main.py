from fastapi import FastAPI
import redis
import os

app = FastAPI()

# Railway injects this variable from the Redis service.
# Make sure you have created a REDIS_URL variable in the
# docker-compose-api service that references Redis -> REDIS_URL.
redis_url = os.environ["REDIS_URL"]

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
def healthz():
    try:
        r.ping()
        return {
            "status": "ok",
            "redis": "up"
        }
    except Exception:
        return {
            "status": "error",
            "redis": "down"
        }