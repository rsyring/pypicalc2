from keg.db import db
import sqlalchemy as sa
import sqlalchemy.orm as saorm

from .utils import DefaultColsMixin, MethodsMixin

MONEY = sa.Numeric(12, 2)


class EntityMixin(DefaultColsMixin, MethodsMixin):
    pass


class Publisher(db.Model, EntityMixin):
    __tablename__ = 'publishers'

    name = sa.Column(sa.Unicode(250), nullable=False, unique=True)


class Person(db.Model, EntityMixin):
    __tablename__ = 'people'

    name = sa.Column(sa.Unicode(250), nullable=False, unique=True)
    email = sa.Column(sa.Unicode(250), nullable=False)

    row_type = sa.Column(sa.String(50), nullable=False)
    __mapper_args__ = {
        'polymorphic_identity': 'person',
        'polymorphic_on': row_type
    }


class Author(Person):
    __tablename__ = 'authors'
    __mapper_args__ = {
        'polymorphic_identity': 'author',
    }

    id = sa.Column(sa.ForeignKey(Person.id, ondelete='cascade'), primary_key=True)


class Book(db.Model, EntityMixin):
    __tablename__ = 'books'

    name = sa.Column(sa.Unicode(250), nullable=False, unique=True)
    is_published = sa.Column(sa.Boolean, nullable=False, default=False)


class Order(db.Model, EntityMixin):
    __tablename__ = 'orders'

    ident = sa.Column(sa.Unicode(250), nullable=False, unique=True)
    is_complete = sa.Column(sa.Boolean, nullable=False, default=False)
