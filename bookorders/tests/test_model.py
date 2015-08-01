from bookorders.model.utils import (
    ColumnCheck,
    EntityBase
)

import bookorders.model.entities as ents


class TestPublisher(EntityBase):
    entity_cls = ents.Publisher
    column_checks = [
        ColumnCheck('name', unique=True),
    ]
