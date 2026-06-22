from fastapi import Request, status
from fastapi.responses import JSONResponse
from src.service_layer.services import InvalidSku

async def invalid_sku_handler(request: Request, exc: InvalidSku):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": f"Invalid sku {exc.sku}"},
    )