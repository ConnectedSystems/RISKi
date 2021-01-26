"""Schema definition for Exposure."""
import enum

from sqlalchemy import (Column, String, Integer, Date, Enum, Float, Boolean,
                        DateTime, Interval, String, Text, ForeignKey, VARCHAR)
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry, Raster

from .base import Base, LiberalBoolean
from .common import OccupancyEnum


# Enums
CalcMethodEnum = enum.Enum("CalcMethodEnum", [
    ("Buildings", "Buildings"),
    ("Indicators", "Indicators"),
    ("Infrastructure", "Infrastructure"),
    ("Crops, livestock and forestry", "Crops, livestock and forestry")
])


# Schema Tables
class ExposureModel(Base):
    __tablename__ = 'exposure_model'
    __table_args__ = ({"schema": "exposure"})

    exposure_model_id = Column('id', Integer, primary_key=True, autoincrement=True)

    name = Column(VARCHAR, nullable=False)
    description = Column(VARCHAR)
    taxonomy_source = Column(VARCHAR)
    category = Column(Enum("buildings", 
                           "indicators", 
                           "infrastructure", 
                           "crops, livestock and forestry",
                           name="category_enum",
                           create_type=True), 
                      nullable=False)
    area_type = Column(VARCHAR)
    area_unit = Column(VARCHAR)
    tag_names = Column(VARCHAR)
    use = Column(Enum(OccupancyEnum))


class Contribution(Base):
    __tablename__ = 'contribution'
    __table_args__ = ({"schema": "exposure"})

    contribution_id = Column('id', Integer, primary_key=True, autoincrement=True)

    exposure_model_id = Column(Integer, ForeignKey("exposure.exposure_model.id"), nullable=False)
    model_source = Column(VARCHAR, nullable=False)
    model_date = Column(Date, nullable=False)
    notes = Column(Text)
    version = Column(VARCHAR)
    purpose = Column(Text)
    project = Column(VARCHAR)
    country_iso = Column(VARCHAR, ForeignKey('common.iso.code'), nullable=False)
    contributed_at = Column(DateTime, nullable=False)
    license_code = Column(VARCHAR, ForeignKey("common.license.code"), nullable=False)
    published = Column(LiberalBoolean, default=True)


class ModelCostType(Base):
    __tablename__ = 'model_cost_type'
    __table_args__ = ({"schema": "exposure"})

    model_cost_type_id = Column('id', Integer, primary_key=True, autoincrement=True)

    exposure_model_id = Column(Integer, ForeignKey("exposure.exposure_model.id"), nullable=False)
    cost_type_name = Column(VARCHAR, nullable=False)
    aggregation_type = Column(VARCHAR, nullable=False)
    unit = Column(VARCHAR)


class Asset(Base):
    __tablename__ = 'asset'
    __table_args__ = ({"schema": "exposure"})

    asset_id = Column('id', Integer, primary_key=True, autoincrement=True)

    exposure_model_id = Column(Integer, ForeignKey("exposure.exposure_model.id"), nullable=False)
    asset_ref = Column(VARCHAR, nullable=False)
    taxonomy = Column(VARCHAR, nullable=False)
    number_of_units = Column(Float)
    area = Column(Float)
    the_geom = Column(Geometry, nullable=False)
    full_geom = Column(Geometry)


class Cost(Base):
    __tablename__ = 'cost'
    __table_args__ = ({"schema": "exposure"})

    cost_id = Column('id', Integer, primary_key=True, autoincrement=True)

    asset_id = Column(Integer, ForeignKey("exposure.asset.id"), nullable=False)
    cost_type_id = Column(Integer, ForeignKey("exposure.model_cost_type.id"), nullable=False)
    value = Column(Float, nullable=False)
    deductible = Column(Float)
    insurance_limit = Column(Float)


class Occupancy(Base):
    __tablename__ = 'occupancy'
    __table_args__ = ({"schema": "exposure"})

    occupancy_id = Column('id', Integer, primary_key=True, autoincrement=True)

    asset_id = Column(Integer, ForeignKey("exposure.asset.id"), nullable=False)
    period = Column(VARCHAR, nullable=False)
    occupants = Column(Float, nullable=False)


class Tags(Base):
    __tablename__ = 'tags'
    __table_args__ = ({"schema": "exposure"})

    tag_id = Column('id', Integer, primary_key=True, autoincrement=True)

    asset_id = Column(Integer, ForeignKey("exposure.asset.id"), nullable=False)
    name = Column(VARCHAR, nullable=False)
    value = Column(VARCHAR, nullable=False)
