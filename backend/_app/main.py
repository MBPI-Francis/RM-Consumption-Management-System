from fastapi import FastAPI
from backend.api_departments.v1 import router as department_router
from backend.api_users.v1 import router as user_router
from backend.api_warehouses.v1 import router as warehouse_router
from backend.api_raw_materials.v1 import router as raw_material_router
from backend.api_droplist.v1 import router as droplist_router
from backend.api_stock_on_hand.v1 import router as soh_router
from backend.api_product_kinds.v1 import router as product_kind_router
from backend.api_auth_users.v1 import router as auth_router

from backend.api_notes.temp import router as notes_router_temp
from backend.api_computed_details.v1 import router as computed_detail_router
from backend.api_receiving_report.temp import router as temp_receiving_report_router
from backend.api_outgoing_report.temp import router as temp_outgoing_report_router
from backend.api_transfer_form.temp import router as temp_transfer_form_router
from backend.api_preparation_form.temp import router as temp_preparation_form_router
from backend.api_held_form.temp import router as temp_held_form_router
from backend.api_create_view_tables import router as create_view_router
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

# These code includes all the routers/endpoint of the api_computed_details
app.include_router(computed_detail_router.router)

# These code includes all the routers/endpoint of the api_notes_temp
app.include_router(notes_router_temp.router)

# These code includes all the routers/endpoint of the api_auth_users
app.include_router(auth_router.router)

# These code includes all the routers/endpoint of the api_receiving_report
app.include_router(temp_receiving_report_router.router)

# These code includes all the routers/endpoint of the api_outgoing_report
app.include_router(temp_outgoing_report_router.router)

# These code includes all the routers/endpoint of the api_transfer_form
app.include_router(temp_transfer_form_router.router)

# These code includes all the routers/endpoint of the api_preparation_form
app.include_router(temp_preparation_form_router.router)

# These code includes all the routers/endpoint of the api_held_form
app.include_router(temp_held_form_router.router)

# These code includes all the routers/endpoint of the api_create_view_table
app.include_router(create_view_router.router)

# Code for Creating database tables
Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "The Warehouse Program API is perfectly working!"}
