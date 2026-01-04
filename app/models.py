from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from app.database import Base
from datetime import datetime

class Customer(Base):

    __tablename__ = "customer"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __repr__(self) -> str:
        return f"id: {self.id}, name: {self.name}, email: {self.email}, created_at: {self.created_at}"

class Product(Base):

    __tablename__ = "product"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)

    def __repr__(self) -> str:
        return f"id: {self.id}, name: {self.name}, category: {self.category}, price: {self.price}, stock: {self.stock}"

class Order(Base):

    __tablename__ = "order"

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customer.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    total_price = Column(Float, nullable=False)

    def __repr__(self) -> str:
        return f"id: {self.id}, customer_id: {self.customer_id}, created_at: {self.created_at}, total_price: {self.total_price}"

class OrderItem(Base):

    __tablename__ = "order_item"

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("order.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    def __repr__(self) -> str:
        return f"id: {self.id}, product_id: {self.product_id}, quantity: {self.quantity}, price: {self.price}"