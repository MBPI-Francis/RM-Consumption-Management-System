from fastapi import FastAPI
from backend.api_departments.v1 import router as department_router
from backend.api_users.v1 import router as user_router
from backend.api_warehouses.v1 import router as warehouse_router
from backend.api_raw_materials.v1 import router as raw_material_router
from backend.api_droplist.v1 import router as droplist_router
from backend.api_stock_on_hand.v1 import router as soh_router
from backend.api_product_kinds.v1 import router as product_kind_router
from backend.api_notes.v1 import router as notes_router
from backend.settings.database import engine, Base

# Initialize FastAPI app
app = FastAPI(title="Warehouse Program API")

# These code includes all the routers/endpoint of the api_departments
app.include_router(department_router.router)

# These code includes all the routers/endpoint of the api_users
app.include_router(user_router.router)


# These code includes all the routers/endpoint of the api_warehouses
app.include_router(warehouse_router.router)

# These code includes all the routers/endpoint of the api_raw_materials
app.include_router(raw_material_router.router)

# These code includes all the routers/endpoint of the api_droplist
app.include_router(droplist_router.router)

# These code includes all the routers/endpoint of the api_stock_on_hand
app.include_router(soh_router.router)

# These code includes all the routers/endpoint of the api_product_kind
app.include_router(product_kind_router.router)

# These code includes all the routers/endpoint of the api_notes
app.include_router(notes_router.router)

# Code for Creating database tables
Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "Welcome to the Backend API Hello HAHAHAHA"}
