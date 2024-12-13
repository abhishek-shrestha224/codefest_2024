from fastapi import FastAPI
from src.auth.routes import auth_router
from src.geofences.routes import geofences_router

app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "Hello World!"}


app.include_router(auth_router, prefix="/auth")
app.include_router(geofences_router, prefix="/geofences")
