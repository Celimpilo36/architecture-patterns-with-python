from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from src.entrypoints import dependancies
from ..schemas.allocatiom_schema import allocationRequest, allocationResponse
from src.service_layer import services
from src.adapters import repository
from src.domain import model

router = APIRouter(prefix="/allocate", tags=["allocate"])

@router.post("/", status_code=201, response_model=allocationResponse)
async def allocate_endpoint(order_line: allocationRequest, session: Session = Depends(dependancies.get_session)):
    repo = repository.SqlAlchemyRepository(session)
    try:
        batch_ref = services.allocate(
            order_line.orderid, order_line.sku, order_line.qty,
            repo, session
            )
        return {"batch_ref": batch_ref}
    except model.OutOfStock as e:
        raise HTTPException(status_code=400, detail=str(e))
    