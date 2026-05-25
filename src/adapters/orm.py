from sqlalchemy import Table, Integer, String, Column, ForeignKey, Date
from sqlalchemy.orm import relationship, registry
from src.domain.model import OrderLine, Batch


mapper_registry = registry()
metadata = mapper_registry.metadata

order_lines = Table(
    'order_lines', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('orderid', String(255)),
    Column('sku', String(255)),
    Column('qty', Integer, nullable=False),
)

batches = Table(
        'batches', metadata,
        Column('id', Integer, primary_key=True),
        Column('reference', String),
        Column('sku', String),
        Column("_purchased_qty", Integer),
        Column("eta", Date, nullable=True)
)

allocations = Table(
        'allocations', metadata,
        Column('batch_id', ForeignKey("batches.id"), primary_key=True),
        Column('orderline_id', ForeignKey("order_lines.id"), primary_key=True),
)


def start_mapper():
    mapper_registry.map_imperatively(
        OrderLine,
        order_lines
        )
    mapper_registry.map_imperatively(
            Batch,
            batches,
            properties={
                "_allocations": relationship(
                    OrderLine,
                    secondary=allocations,
                    collection_class=set
                    )
                }
            )
