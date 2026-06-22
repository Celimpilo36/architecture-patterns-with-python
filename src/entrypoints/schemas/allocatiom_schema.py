from pydantic import BaseModel, ConfigDict

class allocationRequest(BaseModel):
    orderid: str
    sku: str
    qty: int

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

class allocationResponse(BaseModel):
    batch_ref: str