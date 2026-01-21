# backend/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from scraper import AmazonScraper
import logging

logging.basicConfig(level=logging. INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="PriceFighter API", version="0.1.0")

# CORS - allow frontend to call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO:  Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TrackProductRequest(BaseModel):
    url: HttpUrl

class ProductResponse(BaseModel):
    name: str
    price: float
    currency: str
    url: str
    retailer: str

@app.get("/")
def read_root():
    return {"status": "ok", "service": "PriceFighter API"}

@app.post("/api/track", response_model=ProductResponse)
async def track_product(request:  TrackProductRequest):
    """Extract product information from URL"""
    url_str = str(request.url)
    
    logger.info(f"Tracking product:  {url_str}")
    
    # Currently only supports Amazon
    if "amazon.com" not in url_str:
        raise HTTPException(
            status_code=400, 
            detail="Currently only Amazon URLs are supported"
        )
    
    scraper = AmazonScraper()
    
    try:
        product_data = scraper.scrape(url_str)
        
        if not product_data:
            raise HTTPException(
                status_code=400,
                detail="Could not extract product information"
            )
        
        return ProductResponse(**product_data)
        
    except Exception as e:
        logger.error(f"Scraping error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Scraping failed: {str(e)}")

@app.get("/health")
def health_check():
    return {"status": "healthy"}