import enum

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
