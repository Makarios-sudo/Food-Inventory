from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType
from database.database import Base, engine



class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    orders = relationship("Order", back_populates="user")
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default= False)


class Order(Base):
    __tablename__ = 'orders'
    
    ORDER_SIZE = (
        ("SMALL", "SMALL"),
        ("MEDIUM", "MEDIUM"),
        ("LARGE", "LARGE"),
        ("EXTRA_LARGE", "EXTRA_LARGE"),
    )
    
    ORDER_STATUS = (
        ("PENDING", "PENDING"),
        ("IN_TRANSIT", "IN_TRANSIT"),
        ("DELIVERED", "DELIVERED"),
    )

    id = Column(Integer, primary_key=True, index=True)
    # name = Column(String(100), index=True)
    quantity = Column(Integer, nullable=False)
    order_status = Column(ChoiceType(choices=ORDER_STATUS), default="PENDING")
    order_size = Column(ChoiceType(choices=ORDER_SIZE), default="SMALL")
    owner_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="orders")
    
    
Base.metadata.create_all(bind=engine)