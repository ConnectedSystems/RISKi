import enum

from sqlalchemy import event
from sqlalchemy import (Column, String, Integer, Date, Enum, Float, Boolean,
                        DateTime, Interval, String, Text, ForeignKey, VARCHAR)
from sqlalchemy.orm import relationship
# from geoalchemy2 import Geometry, Raster

from .base import Base, LiberalBoolean


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

ComponentEnum = enum.Enum('component_enum', [
    ("Hazard", "Hazard"),
    ("Exposure", "Exposure"),
    ("Vulnerability", "Vulnerability"),
    ("Loss", "Loss")
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


class Contribution(Base):
    __tablename__ = 'contribution'
    __table_args__ = ({"schema": "common"})

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    component = Column(Enum(ComponentEnum), nullable=False, primary_key=True)
    set_id = Column(Integer, nullable=False, primary_key=True)

    model_source = Column(VARCHAR, nullable=False)
    model_date = Column(Date, nullable=False)
    notes = Column(Text)
    version = Column(VARCHAR)
    purpose = Column(Text)
    project = Column(VARCHAR)
    geo_coverage = Column(VARCHAR, nullable=False)  # comma-separated ISO codes indicating regional coverage
    contributed_at_timestamp = Column(DateTime, nullable=False)
    license_code = Column(VARCHAR, ForeignKey("common.license.code"))
    published = Column(LiberalBoolean, default=True)


def load_data(filename):
    import pathlib
    import pandas as pd

    here = str(pathlib.Path(__file__).parent.absolute())
    data = pd.read_csv(here+f'/common_data/{filename}', sep=';').to_dict(orient='records')

    return data


def insert_ISOs(target, connection, **kwargs):
    """Callback function to pre-populate with ISO codes on creation.
    """
    data = load_data("iso.csv")

    connection.execute(
        target.insert(),
        data
    )


def insert_licenses(target, connection, **kwargs):
    data = load_data("license.csv")

    connection.execute(
        target.insert(),
        data
    )

def insert_IMTs(target, connection, **kwargs):
    data = load_data("imt.csv")

    connection.execute(
        target.insert(),
        data
    )

def insert_process_types(target, connection, **kwargs):
    data = load_data("process_type.csv")

    connection.execute(
        target.insert(),
        data
    )


event.listen(ISO.__table__, 'after_create', insert_ISOs)
event.listen(License.__table__, 'after_create', insert_licenses)
event.listen(IMT.__table__, 'after_create', insert_IMTs)
event.listen(ProcessType.__table__, 'after_create', insert_process_types)