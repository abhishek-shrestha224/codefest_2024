from fastapi import FastAPI
from src.auth.routes import auth_router
from src.bbox.routes import bbox_router

app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "Hello World!"}


app.include_router(auth_router, prefix="/auth")
app.include_router(bbox_router, prefix="/bbox")
