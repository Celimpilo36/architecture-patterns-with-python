from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import text, create_engine
from datetime import date
from typing import Optional
from src.adapters import orm

def insert_batch(session: Session, ref: str, sku: str, qty: int, eta: Optional[date]):
    """inserting a batch directly into the databse for testing"""
    session.execute(
        text('INSERT INTO batches (reference, sku, _purchased_qty, eta)'
        'VALUES (:ref, :sku, :qty, :eta)'),
        dict(ref=ref, sku=sku, qty=qty, eta=eta)
    )

def get_allocated_batch_ref(session: Session, orderid: str, sku: str):
    [[orderlineid]] = session.execute(
        text('SELECT id FROM order_line WHERE orderid=:orderid AND sku=:sku'),
        dict(orderid=orderid, sku=sku)   
        )
    
    [[batchref]] = session.execute(
        text(
            'SELECT b.reference FROM allocations JOIN batches AS b ON batch_id = b.id'
            'WHERE orderline_id=:orderlineid'),
            dict(orderlineid=orderid)
    )

    return batchref

def get_session_factory() -> sessionmaker[Session]:
    engine = create_engine("sqlite:///:memory:")
    orm.start_mapper()
    orm.metadata.create_all(engine)

    return sessionmaker(bind=engine)