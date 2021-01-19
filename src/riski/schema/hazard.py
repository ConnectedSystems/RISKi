from sqlalchemy import (Column, String, Integer, Date, Enum, Float, Boolean,
                        DateTime, Interval, String, Text, ForeignKey, VARCHAR)
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry, Raster

from .base import Base


# Schema Tables
class Contribution(Base):
    __tablename__ = 'contribution'
    __table_args__ = ({"schema": "hazard"})

    contribution_id = Column('id', Integer, primary_key=True)
    event_set_id = Column(Integer, ForeignKey('hazard.event_set.id'), nullable=False)

    model_source = Column(VARCHAR, nullable=False)
    model_date = Column(Date, nullable=False)
    notes = Column(Text)
    version = Column(VARCHAR)
    purpose = Column(Text)
    project = Column(VARCHAR)
    contributed_at_timestamp = Column(DateTime, nullable=False)
    license_code = Column(VARCHAR, ForeignKey("common.license.code"))

    children = relationship("EventSet")


class EventSet(Base):
    __tablename__ = 'event_set'
    __table_args__ = ({"schema": "hazard"})

    event_set_id = Column('id', Integer, primary_key=True)

    the_geom = Column(Geometry, nullable=False)
    geographic_area_name = Column(String, nullable=False)
    creation_date = Column(Date, nullable=False)
    hazard_type = Column(String, nullable=False)
    time_start = Column(DateTime)
    time_end = Column(DateTime)
    time_duration = Column(Interval)
    description = Column(Text)
    bibliography = Column(Text)
    is_prob = Column(Boolean, nullable=False)

    children = relationship("Event")


class Event(Base):
    __tablename__ = 'event'
    __table_args__ = ({"schema": "hazard"})

    event_id = Column('id', Integer, primary_key=True)
    event_set_id = Column(Integer, ForeignKey('hazard.event_set.id'))

    calculation_method = Column(Enum("INF", "SIM", "OBS", 
                                     name="calc_method_enum", 
                                     create_type=True),
                                nullable=False)
    frequency = Column(Float)
    occurence_probability = Column(Float)
    occurrence_time_start = Column(DateTime(timezone=False))
    occurrence_time_end = Column(DateTime(timezone=False))
    occurrence_time_span = Column(Interval)
    trigger_hazard_type = Column(VARCHAR, ForeignKey("common.hazard_type.code"))
    trigger_process_type = Column(VARCHAR, ForeignKey("common.process_type.code"))
    trigger_event_id = Column(Integer)
    description = Column(Text)

    children = relationship("FootprintSet")


class FootprintSet(Base):
    __tablename__ = 'footprint_set'
    __table_args__ = ({"schema": "hazard"})

    footprint_set_id = Column('id', Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('hazard.event.id'))

    process_type = Column(VARCHAR, nullable=False)
    imt = Column(VARCHAR, ForeignKey('common.imt.im_code'))
    data_uncertainty = Column(VARCHAR)

    children = relationship("Footprint")


class Footprint(Base):
    __tablename__ = 'footprint'
    __table_args__ = ({"schema": "hazard"})

    footprint_id = Column('id', Integer, primary_key=True)
    footprint_set_id = Column(Integer, ForeignKey('hazard.footprint_set.id'))

    uncertainty_2nd_moment = Column(Float)
    trigger_footprint_id = Column(Integer)

    children = relationship("FootprintData")


class FootprintData(Base):
    __tablename__ = 'footprint_data'
    __table_args__ = ({"schema": "hazard"})

    footprint_data_id = Column('id', Integer, primary_key=True)
    footprint_id = Column(Integer, ForeignKey('hazard.footprint.id'))

    raster = Column(Raster, nullable=False)
    filename = Column(VARCHAR)

