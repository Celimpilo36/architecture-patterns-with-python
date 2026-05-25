from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.config import settings
from src.domain import model
from src.adapters import orm, repository
from pydantic import BaseModel, ConfigDict


orm.start_mapper()
engine = create_engine(settings.database_url, echo=False)
orm.metadata.create_all(engine)

app = FastAPI(title="Allocation Service")


class OrderLineRequest(BaseModel):
    orderid: str
    sku: str
    qty: int

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class AllocationResponse(BaseModel):
    batchref: str

def is_invalid_sku(sku_string, batches):
    return sku_string in {b.sku for b in batches}


@app.post("/allocate", status_code=201, response_model=AllocationResponse)
async def allocate_endpoint(order_line: OrderLineRequest):
    session = Session(engine)
    batches = repository.SqlAlchemyRepository(session=session).list()
    line = model.OrderLine(
                orderid=order_line.orderid,
                sku=order_line.sku,
                qty=order_line.qty
                )
    if not is_invalid_sku(line.sku, batches):
        raise HTTPException(status_code=400, detail=f'Invalid sku {line.sku}')

    try:
        batchref = model.allocate(line, batches)
        session.commit()
        return {'batchref': batchref}

    except model.OutOfStock as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        session.close()
