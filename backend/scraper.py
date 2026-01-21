# backend/scraper.py
import requests
from bs4 import BeautifulSoup
import re
import logging
from typing import Optional, Dict, Any, Tuple

logger = logging.getLogger(__name__)

class AmazonScraper:
    """Scrapes product information from Amazon"""
    
    # Currency symbol to code mapping - ORDER MATTERS!
    # Longer symbols should come before shorter ones to avoid partial matches
    CURRENCY_MAP = {
        # Sri Lankan Rupee (MUST come before 'R' to avoid ZAR match)
        'Rs.': 'LKR',
        'Rs': 'LKR',
        'රු. ': 'LKR',
        'රු': 'LKR',
        'LKR': 'LKR',
        
        # Brazilian Real (MUST come before 'R')
        'R$': 'BRL',
        'BRL': 'BRL',
        
        # South African Rand (comes AFTER Rs and R$)
        'R': 'ZAR',
        'ZAR': 'ZAR',
        
        # Other currencies
        '$': 'USD',
        'USD': 'USD',
        '€': 'EUR',
        'EUR': 'EUR',
        '£': 'GBP',
        'GBP': 'GBP',
        '¥': 'JPY',
        'JPY': 'JPY',
        '₹': 'INR',
        'INR': 'INR',
        'A$': 'AUD',
        'AUD': 'AUD',
        'C$': 'CAD',
        'CAD': 'CAD',
        'S$': 'SGD',
        'SGD': 'SGD',
        'RM': 'MYR',
        'MYR': 'MYR',
        '₱': 'PHP',
        'PHP': 'PHP',
        '฿': 'THB',
        'THB': 'THB',
        'kr':  'SEK',
        'SEK': 'SEK',
        'zł': 'PLN',
        'PLN': 'PLN',
        'د.إ': 'AED',
        'AED': 'AED',
        'SR': 'SAR',
        'SAR': 'SAR',
    }
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept':  'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }
    
    def scrape(self, url: str) -> Optional[Dict[str, Any]]: 
        """
        Scrape product name and price from Amazon URL
        
        Returns:
            dict with keys:  name, price, currency, url, retailer
            None if scraping fails
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response. raise_for_status()
            
            # Decode bytes to string for BeautifulSoup
            soup = BeautifulSoup(response.content. decode('utf-8'), 'html.parser')
            
            # Extract product name
            name = self._extract_name(soup)
            
            # Extract price AND currency
            price, currency = self._extract_price_and_currency(soup)
            
            if not name or price is None:
                logger.warning(f"Could not extract name or price from {url}")
                return None
            
            return {
                'name': name,
                'price': price,
                'currency': currency,
                'url': url,
                'retailer': 'Amazon'
            }
            
        except Exception as e:
            logger.error(f"Error scraping {url}: {str(e)}")
            raise
    
    def _extract_name(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract product name from Amazon page"""
        selectors = [
            '#productTitle',
            '#title',
            'span#productTitle',
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return element.text.strip()
        
        return None
    
    def _extract_price_and_currency(self, soup: BeautifulSoup) -> Tuple[Optional[float], str]:
        """
        Extract price and currency from Amazon page
        
        Returns:
            Tuple of (price, currency_code)
        """
        
        # Strategy 1: Try a-price with offscreen (most reliable)
        price_offscreen = soup.select_one('.a-price .a-offscreen')
        if price_offscreen:
            text = price_offscreen.text. strip()
            price, currency = self._parse_price_text(text)
            if price is not None:
                return price, currency
        
        # Strategy 2: Try whole + fraction with currency symbol
        price_symbol = soup.select_one('.a-price-symbol')
        whole = soup.select_one('.a-price-whole')
        fraction = soup.select_one('.a-price-fraction')
        
        if whole: 
            # Extract currency from symbol element
            currency = 'USD'  # default
            if price_symbol:
                symbol = price_symbol.text.strip()
                currency = self._get_currency_code(symbol)
            
            # whole. text might be "249." or "2,164"
            whole_text = whole.text.strip().replace(',', '')
            
            # Remove currency symbols that might be in the text
            for symbol in ['$', 'Rs', 'රු', '€', '£', '¥', '₹']: 
                whole_text = whole_text.replace(symbol, '')
            
            # Remove trailing dot if present
            if whole_text.endswith('.'):
                whole_text = whole_text[:-1]
            
            if fraction:
                # Combine:  "249" + "." + "00" = "249.00"
                price_str = whole_text + '.' + fraction.text.strip()
            else:
                # No fraction, use whole as-is
                price_str = whole_text
            
            try: 
                return float(price_str), currency
            except ValueError:
                logger.warning(f"Could not parse price: {price_str}")
        
        # Strategy 3: Look for any price pattern on page
        text = soup.get_text()
        
        # Try to find price with various currency symbols
        patterns = [
            (r'(Rs\. ? )\s*([\d,]+\.?\d{0,2})', 'LKR'),  # Sri Lankan Rupee
            (r'(රු\.?)\s*([\d,]+\.?\d{0,2})', 'LKR'),  # Sinhala Rupee
            (r'\$\s*([\d,]+\.?\d{0,2})', 'USD'),  # USD
            (r'€\s*([\d,]+\. ?\d{0,2})', 'EUR'),  # EUR
            (r'£\s*([\d,]+\.?\d{0,2})', 'GBP'),  # GBP
            (r'₹\s*([\d,]+\.?\d{0,2})', 'INR'),  # INR
        ]
        
        for pattern, currency_code in patterns:
            matches = re.findall(pattern, text)
            if matches: 
                try:
                    if isinstance(matches[0], tuple):
                        amount = matches[0][1]
                    else:
                        amount = matches[0]
                    return float(amount. replace(',', '')), currency_code
                except (ValueError, IndexError):
                    continue
        
        return None, 'USD'
    
    def _parse_price_text(self, text: str) -> Tuple[Optional[float], str]:
        """
        Parse price text like "Rs. 2,164.45" or "$249.00"
        
        Returns:
            Tuple of (price, currency_code)
        """
        # Find currency symbol - check LONGEST matches first
        currency = 'USD'  # default
        
        # Sort by length descending to check "Rs." before "Rs" before "R"
        sorted_symbols = sorted(self.CURRENCY_MAP.keys(), key=len, reverse=True)
        
        for symbol in sorted_symbols: 
            if symbol in text:
                currency = self.CURRENCY_MAP[symbol]
                text = text.replace(symbol, '').strip()
                break
        
        # Extract numeric value
        match = re.search(r'([\d,]+\.?\d{0,2})', text)
        if match:
            try: 
                price = float(match.group(1).replace(',', ''))
                return price, currency
            except ValueError:
                pass
        
        return None, currency
    
    def _get_currency_code(self, symbol: str) -> str:
        """Convert currency symbol to currency code"""
        symbol = symbol.strip()
        
        # Sort by length descending to match longer symbols first
        sorted_symbols = sorted(self. CURRENCY_MAP.keys(), key=len, reverse=True)
        
        # Try exact match first
        if symbol in self.CURRENCY_MAP:
            return self. CURRENCY_MAP[symbol]
        
        # Try partial match with longer symbols prioritized
        for key in sorted_symbols:
            if symbol == key:   # Exact match
                return self.CURRENCY_MAP[key]
        
        # Then try startswith matching
        for key in sorted_symbols:
            if symbol. startswith(key):
                return self.CURRENCY_MAP[key]
        
        # Default to USD if unknown
        logger.warning(f"Unknown currency symbol: {symbol}, defaulting to USD")
        return 'USD'