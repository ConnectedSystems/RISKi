from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import CreateSchema
from sqlalchemy import event, DDL

Base = declarative_base()


# Directive to create schemas if they do not exist
event.listen(Base.metadata, 'before_create', DDL("CREATE SCHEMA IF NOT EXISTS common"))
event.listen(Base.metadata, 'before_create', DDL("CREATE SCHEMA IF NOT EXISTS exposure"))
event.listen(Base.metadata, 'before_create', DDL("CREATE SCHEMA IF NOT EXISTS hazard"))
event.listen(Base.metadata, 'before_create', DDL("CREATE SCHEMA IF NOT EXISTS loss"))
event.listen(Base.metadata, 'before_create', DDL("CREATE SCHEMA IF NOT EXISTS vulnerability"))

