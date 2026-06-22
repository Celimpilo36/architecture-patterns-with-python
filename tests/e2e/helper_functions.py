from uuid import uuid4
from sqlalchemy import text, create_engine
from src.config import settings
from sqlalchemy.orm import Session

engine = create_engine(settings.database_url, echo=False)

def get_session() -> Session:
    return Session(engine)

def random_suffix() -> str:
    return uuid4().hex[:6]

def random_sku(name="") -> str:
    return f"sku-{name}-{random_suffix()}"

def random_batchref(name="") -> str:
    return f"batch-{name}-{random_suffix()}"

def random_oderid(name="") -> str:
    return f"order-{name}-{random_suffix()}"

added_batches = []
added_skus = set()

def add_stock(lines)-> None:
    for ref, sku, qty, eta in lines:
        with Session(engine) as session:
                session.execute(
                        text(
                        """
                        INSERT INTO batches (reference, sku, _purchased_qty, eta)
                        VALUES (:ref, :sku, :qty, :eta)
                        """
                        ),
                        {"ref": ref, "sku": sku, "qty": qty, "eta": eta}
                        )
                result = session.execute(
                        text("SELECT id FROM batches WHERE reference = :ref AND sku = :sku"),
                        {"ref":ref, "sku": sku}
                        )
                [[batch_id]] = result.all()
                added_batches.append(batch_id)
                added_skus.add(sku)
                session.commit()
