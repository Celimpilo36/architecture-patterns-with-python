from fastapi import FastAPI
from .routers.allocate import router
from .routers.exceptions import invalid_sku_handler
from src.service_layer.services import InvalidSku

# initializing application 
app = FastAPI(title="Allocation Service")

# adding app routers
app.include_router(router)

# adding exception hadlers
app.add_exception_handler(InvalidSku, invalid_sku_handler) # type: ignore
