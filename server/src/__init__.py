from fastapi import FastAPI
from .auth.routes import auth_router
from .bbox.routes import bbox_router
from .locations.routes import location_router
from .trips.routes import trip_router

app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "Hello World!"}


app.include_router(auth_router, prefix="/auth")
app.include_router(bbox_router, prefix="/bboxes")
app.include_router(location_router, prefix="/locations")
app.include_router(trip_router, prefix="/trips")
