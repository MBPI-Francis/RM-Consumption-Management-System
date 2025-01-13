from fastapi import FastAPI
from backend.api_departments.v1 import router as department_router
from backend.api_users.v1 import router as user_router
from backend.api_warehouses.v1 import router as warehouse_router
from backend.settings.database import engine, Base

# Initialize FastAPI app
app = FastAPI(title="Backend API with Versioning")

# These code includes all the routers/endpoint of the api_departments
app.include_router(department_router.router)

# These code includes all the routers/endpoint of the api_users
app.include_router(user_router.router)


# These code includes all the routers/endpoint of the api_warehouses
app.include_router(warehouse_router.router)

# Code for Creating database tables
Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "Welcome to the Backend API Hello HAHAHAHA"}
