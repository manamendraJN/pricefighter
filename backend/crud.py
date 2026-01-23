# backend/crud.py
from sqlalchemy.orm import Session
from sqlalchemy import desc
from models import Product, PriceHistory
from datetime import datetime
from typing import List, Optional

def get_product_by_url(db: Session, url: str) -> Optional[Product]:
    """Get product by URL"""
    return db.query(Product).filter(Product.url == url).first()

def get_product_by_id(db: Session, product_id: int) -> Optional[Product]:
    """Get product by ID"""
    return db.query(Product).filter(Product.id == product_id).first()

def get_all_products(db: Session, skip: int = 0, limit: int = 100) -> List[Product]:
    """Get all tracked products"""
    return db.query(Product).order_by(desc(Product.updated_at)).offset(skip).limit(limit).all()

def create_product(
    db: Session,
    url: str,
    name: str,
    price: float,
    currency: str,
    retailer: str
) -> Product:
    """Create new product and record initial price"""
    product = Product(
        url=url,
        name=name,
        current_price=price,
        lowest_price=price,
        highest_price=price,
        currency=currency,
        retailer=retailer,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        last_checked_at=datetime.utcnow()
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    
    # Record initial price in history
    add_price_history(db, product.id, price, currency)
    
    return product

def update_product_price(
    db: Session,
    product: Product,
    new_price: float,
    currency: str
) -> Product:
    """Update product price and record in history"""
    # Direct assignment works with Mapped[] types
    product.current_price = new_price
    product.currency = currency
    product.last_checked_at = datetime.utcnow()
    product.updated_at = datetime.utcnow()
    
    # Update lowest/highest - use 'is not None' for proper conditional checks
    if product.lowest_price is None or new_price < product.lowest_price:
        product.lowest_price = new_price
    if product.highest_price is None or new_price > product.highest_price:
        product.highest_price = new_price
    
    db.commit()
    db.refresh(product)
    
    # Record price in history (only if price changed)
    add_price_history(db, product.id, new_price, currency)
    
    return product

def add_price_history(
    db: Session,
    product_id: int,
    price: float,
    currency: str
) -> PriceHistory:
    """Add price history record"""
    history = PriceHistory(
        product_id=product_id,
        price=price,
        currency=currency,
        recorded_at=datetime.utcnow()
    )
    db.add(history)
    db.commit()
    db.refresh(history)
    return history

def get_price_history(
    db: Session,
    product_id: int,
    limit: int = 100
) -> List[PriceHistory]:
    """Get price history for a product"""
    return (
        db.query(PriceHistory)
        .filter(PriceHistory.product_id == product_id)
        .order_by(desc(PriceHistory.recorded_at))
        .limit(limit)
        .all()
    )

def delete_product(db: Session, product_id: int) -> bool:
    """Delete product and its history"""
    product = get_product_by_id(db, product_id)
    if product:
        db.delete(product)
        db.commit()
        return True
    return False