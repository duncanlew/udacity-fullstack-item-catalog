from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


class ComputerShop(Base):
    __tablename__ = "computer_shop"
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)


class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(250))
    price = Column(String(8))
    computer_shop = relationship(ComputerShop)
    computer_shop_id = Column(Integer, ForeignKey('computer_shop.id'))
