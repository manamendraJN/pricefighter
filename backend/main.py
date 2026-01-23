# backend/main.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

import schemas
import crud
from database import get_db, engine, Base
from scraper import AmazonScraper

import logging

logging.basicConfig(level=logging. INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="PriceFighter API", version="0.2. 0")

# Create tables on startup
Base.metadata.create_all(bind=engine)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "ok", "service": "PriceFighter API", "version": "0.2.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/api/track", response_model=schemas.ProductTrackResponse)
async def track_product(
    request: schemas.TrackProductRequest,
    db: Session = Depends(get_db)
):
    """Track Amazon product - saves to database"""
    url_str = str(request.url)
    
    logger.info(f"Tracking product: {url_str}")
    
    if "amazon" not in url_str. lower():
        raise HTTPException(
            status_code=400,
            detail="Currently only Amazon URLs are supported"
        )
    
    scraper = AmazonScraper()
    
    try:
        # Scrape product data
        product_data = scraper.scrape(url_str)
        
        if not product_data:
            raise HTTPException(
                status_code=400,
                detail="Could not extract product information"
            )
        
        # Check if product already exists
        existing_product = crud.get_product_by_url(db, url_str)
        
        if existing_product:
            # Update existing product with new price
            updated_product = crud. update_product_price(
                db,
                existing_product,
                product_data['price'],
                product_data['currency']
            )
            logger.info(f"Updated product #{updated_product.id}")
            
            return schemas.ProductTrackResponse(
                name=updated_product.name,
                price=updated_product.current_price,
                currency=updated_product.currency,
                url=updated_product.url,
                retailer=updated_product.retailer,
                tracked=True,
                product_id=updated_product.id
            )
        else:
            # Create new product
            new_product = crud.create_product(
                db,
                url=url_str,
                name=product_data['name'],
                price=product_data['price'],
                currency=product_data['currency'],
                retailer=product_data['retailer']
            )
            logger.info(f"Created new product #{new_product.id}")
            
            return schemas.ProductTrackResponse(
                name=new_product.name,
                price=new_product.current_price,
                currency=new_product.currency,
                url=new_product.url,
                retailer=new_product.retailer,
                tracked=True,
                product_id=new_product.id
            )
        
    except Exception as e: 
        logger.error(f"Scraping error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Scraping failed: {str(e)}")

@app.get("/api/products", response_model=List[schemas.ProductResponse])
def get_products(
    skip:  int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all tracked products"""
    products = crud. get_all_products(db, skip=skip, limit=limit)
    return products

@app. get("/api/products/{product_id}", response_model=schemas. ProductWithHistoryResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get product details with price history"""
    product = crud.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.get("/api/products/{product_id}/history", response_model=List[schemas. PriceHistoryResponse])
def get_product_history(
    product_id: int,
    limit: int = 100,
    db:  Session = Depends(get_db)
):
    """Get price history for a product"""
    product = crud.get_product_by_id(db, product_id)
    if not product: 
        raise HTTPException(status_code=404, detail="Product not found")
    
    history = crud.get_price_history(db, product_id, limit=limit)
    return history

@app.delete("/api/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Delete a tracked product"""
    success = crud.delete_product(db, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"status": "deleted", "product_id": product_id}