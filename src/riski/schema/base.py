from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import CreateSchema
from sqlalchemy import event, DDL, TypeDecorator, Boolean

Base = declarative_base()


class LiberalBoolean(TypeDecorator):
    """Allows strings to be interpreted as true/false values.

    See: https://docs.sqlalchemy.org/en/13/changelog/migration_12.html?highlight=hard%20typeerror
    """
    impl = Boolean

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = bool(value)
        return value


# Directive to create schemas if they do not exist
event.listen(Base.metadata, 'before_create', DDL("CREATE SCHEMA IF NOT EXISTS common"))
event.listen(Base.metadata, 'before_create', DDL("CREATE SCHEMA IF NOT EXISTS exposure"))
event.listen(Base.metadata, 'before_create', DDL("CREATE SCHEMA IF NOT EXISTS hazard"))
event.listen(Base.metadata, 'before_create', DDL("CREATE SCHEMA IF NOT EXISTS loss"))
event.listen(Base.metadata, 'before_create', DDL("CREATE SCHEMA IF NOT EXISTS vulnerability"))
