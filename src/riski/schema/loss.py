"""Loss schema."""

import enum

from sqlalchemy import (Column, String, Integer, Date, Enum, Float, Boolean,
                        DateTime, Interval, String, Text, ForeignKey, VARCHAR, BigInteger)
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry, Raster

from .base import Base, LiberalBoolean
from .common import OccupancyEnum


# Enums
ComponentEnum = enum.Enum("component_enum", [
    ("Buildings", "Buildings"), 
    ("Indicator", "Indicator"), 
    ("Infrastructure", "Infrastructure"),
    ("Crops, livestock and forestry", "Crops, livestock and forestry")
])

FrequencyEnum = enum.Enum("frequency_enum", [
    ("Rate of Exceedence", "Rate of Exceedence"),
    ("Probability of Exceedence", "Probability of Exceedence"),
    ("Return Period", "Return Period"),
])

MetricEnum = enum.Enum("metric_enum", [
    ("AAL", "AAL"),
	("AALR", "AALR"),
	("PML", "PML")
])

LossTypeEnum = enum.Enum("loss_type_enum", [
    ("Ground Up", "Ground Up"),
	("Insured", "Insured")]
)


# Schema tables
class Contribution(Base):
    __tablename__ = 'Contribution'
    __table_args__ = ({"schema": "loss"})

    contribution_id = Column('id', Integer, primary_key=True, autoincrement=True)

    loss_model_id = Column(Integer, ForeignKey('loss.loss_model.id'), nullable=False)
    model_source = Column(VARCHAR, nullable=False)
    model_date = Column(Date, nullable=False)
    notes = Column(Text)
    version = Column(VARCHAR)
    purpose = Column(Text)
    project = Column(VARCHAR)
    country_iso = Column(VARCHAR, ForeignKey('common.iso.code'), nullable=False)
    contributed_at = Column(DateTime, nullable=False)
    license_code = Column(VARCHAR, ForeignKey('common.license.code'))
    published = Column(LiberalBoolean, default=True)


class LossModel(Base):
    __tablename__ = 'loss_model'
    __table_args__ = ({"schema": "loss"})

    loss_model_id = Column('id', Integer, primary_key=True, autoincrement=True)

    name = Column(VARCHAR, nullable=False)
    description = Column(Text)
    hazard_type = Column(VARCHAR, ForeignKey('common.hazard_type.code'))
    process_type = Column(VARCHAR, ForeignKey('common.process_type.code'))
    hazard_link = Column(VARCHAR)
    exposure_link = Column(VARCHAR)
    vulnerability_link = Column(VARCHAR)


class LossMap(Base):
    __tablename__ = 'loss_map'
    __table_args__ = ({"schema": "loss"})

    loss_map_id = Column('id', Integer, primary_key=True, autoincrement=True)

    loss_model_id = Column(Integer, ForeignKey('loss.loss_model.id'), nullable=False)
    occupancy = Column(Enum(OccupancyEnum), nullable=False)
    component = Column(Enum(ComponentEnum), nullable=False)
    loss_type = Column(Enum(LossTypeEnum), nullable=False)
    return_period = Column(Integer)  # Return period in years
    units = Column(VARCHAR, nullable=False)
    metric = Column(Enum(MetricEnum), nullable=False)


class LossMapValues(Base):
    __tablename__ = 'loss_map_values'
    __table_args__ = ({"schema": "loss"})

    loss_map_values_id = Column('id', BigInteger, primary_key=True, autoincrement=True)

    loss_map_id = Column(Integer, ForeignKey('loss.loss_map.id'), nullable=False)
    asset_ref = Column(VARCHAR)
    loss = Column(Float, nullable=False)
    the_geom = Column(Geometry, nullable=False)


class LossCurveMap(Base):
    __tablename__ = 'loss_curve_map'
    __table_args__ = ({"schema": "loss"})

    loss_curve_map_id = Column('id', Integer, primary_key=True, autoincrement=True)

    loss_model_id = Column(Integer, ForeignKey('loss.loss_model.id'), nullable=False)
    occupancy = Column(Enum(OccupancyEnum), nullable=False)
    component = Column(Enum(ComponentEnum), nullable=False)
    loss_type = Column(Enum(LossTypeEnum), nullable=False)
    frequency = Column(Enum(FrequencyEnum), nullable=False)
    investigation_time = Column(Integer)
    units = Column(VARCHAR, nullable=False)


class LossCurveMapValues(Base):
    __tablename__ = 'loss_curve_map_values'
    __table_args__ = ({"schema": "loss"})

    loss_curve_map_values_id = Column('id', BigInteger, primary_key=True, autoincrement=True)

    loss_curve_map_id = Column(Integer, nullable=False)
    asset_ref = Column(VARCHAR)
    losses = Column(VARCHAR, nullable=False)
    rates = Column(Float, nullable=False)
    the_geom = Column(Geometry, nullable=False)


# View: all_loss_map_values

