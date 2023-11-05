from database import Base
from sqlalchemy import TIMESTAMP, Column, String, Integer, ForeignKey
from sqlalchemy.sql import func


class Courier(Base):
    __tablename__ = 'couriers'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    courier_name = Column(String, nullable=False)


class Region(Base):
    __tablename__ = 'regions'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    region_name = Column(String, nullable=False)


class Order(Base):
    __tablename__ = 'orders'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    courier_id = Column(ForeignKey('couriers.id'), primary_key=True)
    region_id = Column(ForeignKey('regions.id'), primary_key=True)
    order_text = Column(String, nullable=False)
    start_time = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=func.now())
    finish_time = Column(TIMESTAMP(timezone=True),
                         default=None, onupdate=func.now())

class CourierRegion(Base):
    __tablename__ = 'courier_region'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    courier_id = Column(ForeignKey('couriers.id'), primary_key=True)
    region_id = Column(ForeignKey('regions.id'), primary_key=True)
