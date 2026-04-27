from fastapi import FastAPI, status
from database import Base, engine
from routers import posts

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(posts.router, prefix="/api/posts", tags=["posts"])

@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    return {
        "message": "service is running"
    }