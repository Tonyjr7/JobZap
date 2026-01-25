from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Database imports
from database.database import engine
from database.base import Base

# Import routers
from route.fetcher import router as fetcher_router
from route.extract import extractor_router

# Initialize FastAPI app
app = FastAPI()

# Add the CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],         # List of allowed origins
    allow_credentials=True,        # Allow cookies to be sent with requests
    allow_methods=["*"],           # Allow all HTTP methods
    allow_headers=["*"],           # Allow all headers
)

# Create database tables on startup
@app.on_event("startup")
def on_startup():
    from database.models.job import Job
    Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(fetcher_router)
app.include_router(extractor_router)

# Basic root endpoint
@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI application!"}
