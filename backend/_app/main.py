from fastapi import FastAPI
from backend.api_departments.v1 import router as department_router
from backend.settings.database import engine, Base

# Initialize FastAPI app
app = FastAPI(title="Backend API with Versioning")

# Include department router
app.include_router(department_router.router)

# Create database tables
Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "Welcome to the Backend API"}

