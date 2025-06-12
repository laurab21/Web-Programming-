from sqlalchemy import Column, String, Boolean, Integer
from sqlalchemy.orm import relationship
from .base import Base

class User(Base):
    __tablename__ = "users"  # ✅ required

    id = Column(Integer, primary_key=True, index=True)  # ✅ required primary key
    email = Column(String(100), nullable=False, unique=True, index=True)
    hashed_password = Column(String(100), nullable=False)
    full_name = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)

    # Relations
    loans = relationship("Loan", back_populates="user", cascade="all, delete-orphan")

