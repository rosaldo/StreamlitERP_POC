import os

from datetime import datetime as dtt
from sqlalchemy import (Boolean, Column, DateTime, Double, ForeignKey, Integer,
                        String, create_engine)
from sqlalchemy.engine import reflection
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Suppliers(Base):
    version = "1.0.0"
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    address = Column(String)
    phone = Column(String)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=dtt.now())
    updated_at = Column(DateTime)

    def __repr__(self):
        return f"Suppliers(id={self.id}, name={self.name}, email={self.email}, address={self.address}, phone={self.phone}, created_at={self.created_at}, updated_at={self.updated_at})"

class Products(Base):
    version = "1.0.0"
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    supplier = Column(String)
    stock = Column(Double)
    unit = Column(String)
    price = Column(Double)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=dtt.now())
    updated_at = Column(DateTime)

    def __repr__(self):
        return f"Products(id={self.id}, name={self.name}, description={self.description}, supplier={self.supplier}, stock={self.stock}, unit={self.unit}, price={self.price}, created_at={self.created_at}, updated_at={self.updated_at})"

class Costumers(Base):
    version = "1.0.0"
    __tablename__ = "costumers"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    address = Column(String)
    phone = Column(String)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=dtt.now())
    updated_at = Column(DateTime)

    def __repr__(self):
        return f"Costumers(id={self.id}, name={self.name}, email={self.email}, address={self.address}, phone={self.phone}, created_at={self.created_at}, updated_at={self.updated_at})"

class Sales(Base):
    version = "1.0.0"
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True)
    costumer_id = Column(Integer, ForeignKey("costumers.id"))
    price = Column(Double)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=dtt.now())
    updated_at = Column(DateTime)

    def __repr__(self):
        return f"Sales(id={self.id}, costumer={self.costumer}, price={self.price}, created_at={self.created_at}, updated_at={self.updated_at})"

class ProductsSales(Base):
    version = "1.0.0"
    __tablename__ = "products_sales"

    id = Column(Integer, primary_key=True)
    sale_id = Column(Integer, ForeignKey("sales.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=dtt.now())
    updated_at = Column(DateTime)

    def __repr__(self):
        return f"ProductsSales(id={self.id}, sale={self.sale}, product={self.product}, quantity={self.quantity}, created_at={self.created_at}, updated_at={self.updated_at})"

class Database:
    version = "1.0.0"
    suppliers = Suppliers
    products = Products
    costumers = Costumers
    sales = Sales
    products_sales = ProductsSales

    def __init__(self):
        script_name = os.path.basename(__file__)[:-3]
        script_path = os.path.dirname(os.path.realpath(__file__))
        db_name = f"sqlite:///{script_path}{os.sep}{script_name}.sql3"
        self.engine = create_engine(db_name)
        session = sessionmaker(bind=self.engine)
        self.session = session()
        inspector = reflection.Inspector.from_engine(self.engine)
        if Suppliers.__tablename__ not in inspector.get_table_names():
            Suppliers.__table__.create(self.engine)
        if Products.__tablename__ not in inspector.get_table_names():
            Products.__table__.create(self.engine)
        if Costumers.__tablename__ not in inspector.get_table_names():
            Costumers.__table__.create(self.engine)
        if Sales.__tablename__ not in inspector.get_table_names():
            Sales.__table__.create(self.engine)
        if ProductsSales.__tablename__ not in inspector.get_table_names():
            ProductsSales.__table__.create(self.engine)

dbase = Database()
