from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import text, create_engine
from datetime import date
from typing import Optional
from src.adapters import orm

def insert_batch(session: Session, ref: str, sku: str, qty: int, eta: Optional[date]):
    """inserting a batch directly into the databse for testing"""
    session.execute(
        text("""INSERT INTO batches (reference, sku, _purchased_qty, eta)
        VALUES (:reference, :sku, :_purchased_qty, :eta)"""),

         {
             "reference": ref,
             "sku": sku,
             "_purchased_qty": qty,
             "eta": eta
          }
    )

def get_allocated_batch_ref(session: Session, orderid: str, sku: str):
    result = session.execute(
        text("""
             SELECT b.reference
             FROM allocations
             a JOIN batches b ON a.batch_id = b.id
             WHERE a.orderid = :orderid AND b.sku= :sku
             """
             ),
             {"orderid": orderid, "sku":sku}    
        )
    return result.scalar()

def get_session_factory() -> sessionmaker[Session]:
    engine = create_engine("sqlite:///:memory:")
    orm.metadata.create_all(engine)

    return sessionmaker(bind=engine)