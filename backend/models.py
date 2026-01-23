# backend/models.py
from __future__ import annotations
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base
from datetime import datetime
from typing import Optional, List

class Product(Base):
    __tablename__ = "products"
    
    # Use Mapped[] for proper type hints
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    url: Mapped[str] = mapped_column(String, unique=True, index=True)
    name: Mapped[str] = mapped_column(String)
    retailer: Mapped[str] = mapped_column(String)
    currency: Mapped[str] = mapped_column(String)
    current_price: Mapped[float] = mapped_column(Float)
    lowest_price: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    highest_price: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_checked_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationship
    price_history: Mapped[List["PriceHistory"]] = relationship(
        "PriceHistory", 
        back_populates="product",
        cascade="all, delete-orphan"
    )

class PriceHistory(Base):
    __tablename__ = "price_history"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"))
    price: Mapped[float] = mapped_column(Float)
    currency: Mapped[str] = mapped_column(String)
    recorded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationship
    product: Mapped["Product"] = relationship("Product", back_populates="price_history")