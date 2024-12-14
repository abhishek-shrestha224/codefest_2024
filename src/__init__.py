from fastapi import FastAPI
from src.auth.routes import auth_router
from src.locations.routes import location_router
from src.trips.routes import trip_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "Hello World!"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  #
    allow_headers=["*"],
)
app.include_router(auth_router, prefix="/auth")
app.include_router(location_router, prefix="/locations")
app.include_router(trip_router, prefix="/trips")
