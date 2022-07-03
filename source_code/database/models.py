from sqlalchemy import String, Column, ForeignKey, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Buyer(Base):
    __tablename__ = "buyers"

    id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)


class Manager(Base):
    __tablename__ = "managers"

    id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)


class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True)
    model = Column(String, nullable=False)


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True)
    manager_id = Column(Integer, ForeignKey(Manager.id, ondelete='cascade'))
    car_id = Column(Integer, ForeignKey(Car.id, ondelete='cascade'))
    state_number = Column(String, nullable=False)
    buyer_id = Column(Integer, ForeignKey(Buyer.id, ondelete='cascade'))
    date = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
