import datetime as dt
import random

import arrow
from blazeutils.strings import randchars
from collections import namedtuple
from keg import current_app
from keg.db import db
import six
import sqlalchemy as sa
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.inspection import inspect as sainsp
from sqlalchemy.sql import expression
import sqlalchemy.orm as saorm
from sqlalchemy_utils import ArrowType


ColumnCheck = namedtuple('ColumnCheck', 'name, required, fk, unique, timestamp')
ColumnCheck.__new__.__defaults__ = (True, None, None, None)


def session_commit():
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise


def session_flush():
    try:
        db.session.flush()
    except Exception:
        db.session.rollback()
        raise


class utcnow(expression.FunctionElement):
    type = sa.DateTime()


@compiles(utcnow, 'postgresql')
def _pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


@compiles(utcnow, 'mssql')
def _ms_utcnow(element, compiler, **kw):
    return "GETUTCDATE()"


@compiles(utcnow, 'sqlite')
def _sqlite_utcnow(element, compiler, **kw):
    return "CURRENT_TIMESTAMP"


class DefaultColsMixin(object):
    id = sa.Column(sa.Integer, primary_key=True)
    created_utc = sa.Column(ArrowType, nullable=False, default=arrow.now, server_default=utcnow())
    updated_utc = sa.Column(ArrowType, nullable=False, default=arrow.now, onupdate=arrow.now,
                            server_default=utcnow())


class MethodsMixin(object):
    def from_dict(self, data):
        """
        Update an instance with data from a JSON-style nested dict/list
        structure.
        """
        # surrogate can be guessed from autoincrement/sequence but I guess
        # that's not 100% reliable, so we'll need an override

        mapper = saorm.object_mapper(self)

        for key, value in six.iteritems(data):
            if isinstance(value, dict):
                dbvalue = getattr(self, key)
                rel_class = mapper.get_property(key).mapper.class_
                pk_props = rel_class._descriptor.primary_key_properties

                # If the data doesn't contain any pk, and the relationship
                # already has a value, update that record.
                if not [1 for p in pk_props if p.key in data] and \
                   dbvalue is not None:
                    dbvalue.from_dict(value)
                else:
                    record = rel_class.update_or_create(value)
                    setattr(self, key, record)
            elif isinstance(value, list) and \
                    value and isinstance(value[0], dict):

                rel_class = mapper.get_property(key).mapper.class_
                new_attr_value = []
                for row in value:
                    if not isinstance(row, dict):
                        raise Exception(
                            'Cannot send mixed (dict/non dict) data '
                            'to list relationships in from_dict data.'
                        )
                    record = rel_class.update_or_create(row)
                    new_attr_value.append(record)
                setattr(self, key, new_attr_value)
            else:
                setattr(self, key, value)

    @classmethod
    def add(cls, _commit=True, _flush=False, **kwargs):
        o = cls()
        o.from_dict(kwargs)
        db.session.add(o)
        if _flush:
            session_flush()
        elif _commit:
            session_commit()
        return o

    @classmethod
    def delete_all(cls, commit=True):
        retval = cls.query.delete()
        if commit:
            session_commit()
        return retval

    @classmethod
    def testing_create(cls, **kwargs):
        # automatically sets most field types. Any fields passed into the method
        #   will override the automatic behavior
        # subclasses need to set any necessary key values before calling this method
        #   including primary and foreign keys
        insp = sainsp(cls)
        for column in insp.columns:
            # skip fields already in kwargs, foreign key references, and any
            #   field having a default or server_default configured
            if (column.key in kwargs or column.foreign_keys or column.server_default or
                    column.default or column.primary_key):
                continue

            # If the column is being used for polymorphic inheritance identification, then don't
            # set the value.
            if insp.mapper.polymorphic_on is column:
                continue

            if isinstance(column.type, sa.types.Enum):
                kwargs[column.key] = random.choice(column.type.enums)
            elif isinstance(column.type, sa.types.String):
                kwargs[column.key] = randchars(min(column.type.length or 25, 25))
            elif isinstance(column.type, (sa.types.Integer, sa.types.Numeric)):
                kwargs[column.key] = 0
            elif isinstance(column.type, sa.types.Date):
                kwargs[column.key] = dt.date.today()
            elif isinstance(column.type, sa.types.DateTime):
                kwargs[column.key] = dt.datetime.now()

        return cls.add(**kwargs)

    def ensure(self, key, _flush=False, _commit=True):
        cls_columns = sainsp(self).mapper.columns
        key_col = getattr(cls_columns, key)
        key_val = getattr(self, key)
        exiting_record = self.query.filter(key_col == key_val).first()
        if not exiting_record:
            db.session.add(self)
            if _flush:
                session_flush()
            elif _commit:
                session_commit()
            return self
        return exiting_record


def validate_unique_exc(exc):
    return _validate_unique_msg(db.engine.dialect.name, str(exc))


def _validate_unique_msg(dialect, msg):
    """
        Does the heavy lifting for validate_unique_exception().

        Broken out separately for easier unit testing.  This function takes string args.
    """
    if 'IntegrityError' not in msg:
        raise ValueError('"IntegrityError" exception not found')
    if dialect == 'postgresql':
        if 'duplicate key value violates unique constraint' in msg:
            return True
    elif dialect == 'mssql':
        if 'Cannot insert duplicate key' in msg:
            return True
    elif dialect == 'sqlite':
        if 'UNIQUE constraint failed' in msg:
            return True
    else:
        raise ValueError('is_unique_exc() does not yet support dialect: %s' % dialect)
    return False


class EntityBase(object):
    entity_cls = None
    column_checks = None
    timestamp_cols = ('created_utc', 'updated_utc')
    # Set to: 'setup_class', 'setup', or None
    delete_all_on = 'setup_class'

    @classmethod
    def setup_class(cls):
        assert current_app.db_enabled, 'app.db_enabled is False'
        assert cls.entity_cls, 'The entity_cls attribute must be set.'
        assert cls.column_checks, 'column_checks should be defined for this entity'
        if cls.timestamp_cols:
            if cls.column_checks is None:
                cls.column_checks = []
            createdts_col_name, updatedts_col_name = cls.timestamp_cols
            cls.column_checks.append(ColumnCheck(createdts_col_name, timestamp='create'))
            cls.column_checks.append(ColumnCheck(updatedts_col_name, timestamp='update'))
        if cls.delete_all_on:
            cls.ent_delete_all()

    @classmethod
    def ent_delete_all(cls):
        if hasattr(cls.entity_cls, 'delete_cascaded'):
            cls.entity_cls.delete_cascaded()
        else:
            cls.entity_cls.delete_all()

    def setup(self):
        if self.delete_all_on == 'setup':
            self.ent_delete_all()

    def test_add(self):
        self.ent_delete_all()
        o = self.entity_cls.testing_create()
        assert self.entity_cls.query.count() == 1
        if hasattr(self.entity_cls, 'id'):
            assert o.id

    def check_column_null(self, col, is_required):
        assert col.nullable != is_required

    def check_column_unique(self, col, is_unique):
        assert col.unique == is_unique, 'Expected column "{}" to have unique={}'.format(
            col.name, is_unique)

    def check_column_fk(self, col, fk):
        fk_count = len(col.foreign_keys)
        if fk:
            assert fk_count == 1, 'check_column_fk() can not handle colums w/ multiple FKs'
            assert fk == list(col.foreign_keys)[0]._get_colspec()
        else:
            assert not fk_count, 'Didn\'t expect column "{}" to have a foreign key'.format(col.name)

    def check_column_timestamp(self, col, ts_type):
        if not isinstance(col.type, (ArrowType, sa.DateTime)):
            raise AssertionError('Column "{}" is not a recognized timestamp type.'.format(col.name))
        assert col.default
        if ts_type == 'update':
            assert col.onupdate, 'Column "{}" should have onupdate set'.format(col.name)
        assert col.server_default, 'Column "{}" should have server_default set'.format(col.name)

    def test_column_checks(self):
        if not self.column_checks:
            return
        for col_check in self.column_checks:
            col = getattr(self.entity_cls, col_check.name)
            yield self.check_column_null, col, col_check.required
            yield self.check_column_unique, col, col_check.unique
            yield self.check_column_fk, col, col_check.fk
            if col_check.timestamp:
                yield self.check_column_timestamp, col, col_check.timestamp

    def check_unique_constraint(self, **kwargs):
        self.entity_cls.testing_create(**kwargs)
        try:
            self.entity_cls.testing_create(**kwargs)
            raise AssertionError('Uniqueness error was not encountered.')
        except Exception as e:
            if not validate_unique_exc(e):
                raise
