from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from os import getenv

# just import whatever routers you want to import from ./routers here.
import routers.users_router as users_router

# FastAPI instance here, along with CORS middleware
DEBUG = getenv("DEBUG_BACKEND", "False").lower() in ("true", "t", "1")
app = FastAPI(debug=DEBUG, title='Recruitment Management System backend', description='Backend for the RMS-IIITH')
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_methods=["GET", "POST"],
)


# base path for checking if the backend is alive.
@app.get('/', tags=["General"])
async def index():
    return {"message": "hello, you have reached the backend API service. what would you like to order?"}


# mount the imported routers on a path here.
app.include_router(users_router.router, prefix="/user", tags=["User Management"])
