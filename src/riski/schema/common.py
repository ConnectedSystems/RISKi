import enum

from sqlalchemy import event
from sqlalchemy import (Column, String, Integer, Date, Enum, Float, Boolean,
                        DateTime, Interval, String, Text, ForeignKey, VARCHAR)
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry, Raster

from .base import Base

OccupancyEnum = enum.Enum('occupancy_enum', [
    ("Residential", "Residential"),
    ("Commercial", "Commercial"),
    ("Industrial", "Industrial"),
    ("Infrastructure", "Infrastructure"),
    ("Healthcare", "Healthcare"),
    ("Educational", "Educational"),
    ("Government", "Government"),
    ("Crop", "Crop"),
    ("Livestock", "Livestock"),
    ("Forestry", "Forestry"),
    ("Mixed occupancy", "Mixed occupancy")
])


# Schema Tables
class License(Base):
    __tablename__ = 'license'
    __table_args__ = ({"schema": "common"})

    code = Column(VARCHAR, primary_key=True)

    name = Column(VARCHAR, nullable=False)
    notes = Column(Text)
    url = Column(VARCHAR, nullable=False)


class IMT(Base):
    __tablename__ = 'imt'
    __table_args__ = ({"schema": "common"})

    im_code = Column(VARCHAR, primary_key=True)

    process_code = Column(VARCHAR, ForeignKey("common.process_type.code"))
    hazard_code = Column(VARCHAR, nullable=False)
    description = Column(VARCHAR, nullable=False)
    units = Column(VARCHAR, nullable=False)


class ProcessType(Base):
    __tablename__ = 'process_type'
    __table_args__ = ({"schema": "common"})

    code = Column(VARCHAR, primary_key=True)

    hazard_code = Column(VARCHAR, nullable=False)
    name = Column(VARCHAR, nullable=False)


class HazardType(Base):
    __tablename__ = 'hazard_type'
    __table_args__ = ({"schema": "common"})

    code = Column(VARCHAR, primary_key=True)

    name = Column(VARCHAR, nullable=False)


class ISO(Base):
    __tablename__ = 'iso'
    __table_args__ = ({"schema": "common"})

    # ISO 3166 ALPHA-3 country code
    code = Column(VARCHAR, primary_key=True)

    # Country name (in English)
    name = Column(VARCHAR, nullable=False)


def insert_ISOs(target, connection, **kwargs):
    """Callback function to pre-populate with ISO codes on creation.
    """
    connection.execute(
        target.insert(),
        {'code': 'MDG', 'name':'Madagascar'}
    )


def insert_licenses(target, connection, **kwargs):
    connection.execute(
        target.insert(),
        {'code': 'CC BY-SA 4.0', 
         'name':'Creative Commons BY-SA 4.0', 
         'notes': '', 
         'url': ''
        }
    )

def insert_IMTs(target, connection, **kwargs):
    connection.execute(
        target.insert(),
        {'process_code': 'QGM',
         'hazard_code': 'EQ',
         'im_code': 'PGA:g',
         'description': 'Peak ground acceleration in g',
         'units': 'g'
        }
    )

def insert_process_types(target, connection, **kwargs):
    connection.execute(
        target.insert(),
        {'code': 'QGM',
         'hazard_code': 'EQ',
         'name': 'Ground Motion',
        }
    )


event.listen(ISO.__table__, 'after_create', insert_ISOs)
event.listen(License.__table__, 'after_create', insert_licenses)
event.listen(IMT.__table__, 'after_create', insert_IMTs)
event.listen(ProcessType.__table__, 'after_create', insert_process_types)