# 💰 PriceFighter

AI-powered price tracking and negotiation tool that helps you never overpay for Amazon products.

![Status](https://img.shields.io/badge/status-active-success.svg)
![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

---

## 🚀 Features

### ✅ Completed (Step 1 - MVP)

- **Amazon Price Scraping**: Extract product name, price, and currency from any Amazon product URL
- **Multi-Currency Support**:  Automatically detects and supports 15+ currencies (USD, EUR, GBP, LKR, INR, AUD, CAD, SGD, MYR, PHP, THB, BRL, ZAR, PLN, SEK, AED, SAR, JPY)
- **Real-time Price Extraction**: Instant product information retrieval
- **Professional UI**: Clean, modern web interface built with Next.js and Tailwind CSS
- **Mobile Responsive**: Works seamlessly on desktop, tablet, and mobile devices
- **Error Handling**: Robust validation for URLs and scraping failures
- **RESTful API**: Well-documented API endpoints for integration

### 🔄 In Progress

- Price history tracking
- Database persistence
- User authentication
- Price drop alerts

### 📋 Planned

- Browser extension (Chrome, Firefox)
- Automated price negotiation emails
- Multi-retailer support (eBay, Walmart, Best Buy)
- Price comparison across retailers
- Email/SMS notifications
- Webhook integrations

---

## 🛠️ Tech Stack

### Backend
- **Language**: Python 3.8+
- **Framework**: FastAPI
- **Web Scraping**: BeautifulSoup4, Requests
- **Validation**: Pydantic
- **Server**: Uvicorn

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **HTTP Client**: Fetch API

### Infrastructure
- **Version Control**: Git + GitHub
- **Deployment**: Railway (backend), Vercel (frontend)

---

## 📁 Project Structure

```
pricefighter/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── scraper. py           # Amazon scraping logic
│   ├── requirements.txt     # Python dependencies
│   └── . env. example         # Environment variables template
│
├── frontend/
│   ├── app/
│   │   ├── page. tsx         # Landing page
│   │   ├── layout.tsx       # Root layout
│   │   └── globals.css      # Global styles
│   ├── components/
│   │   └── ProductTracker.tsx  # Main tracker component
│   ├── package.json         # Node dependencies
│   └── tailwind.config.ts   # Tailwind configuration
│
├── . gitignore
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.8+**
- **Node.js 18+**
- **npm or yarn**

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows: 
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn main:app --reload --port 8000
```

Backend will be running at **http://localhost:8000**

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create environment file
echo "NEXT_PUBLIC_BACKEND_URL=http://localhost:8000" > .env. local

# Run development server
npm run dev
```

Frontend will be running at **http://localhost:3000**

---

## 📚 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### `GET /`
Health check endpoint

**Response:**
```json
{
  "status": "ok",
  "service": "PriceFighter API"
}
```

---

#### `GET /health`
Service health status

**Response:**
```json
{
  "status": "healthy"
}
```

---

#### `POST /api/track`
Track an Amazon product

**Request:**
```json
{
  "url": "https://www.amazon.com/dp/B0CHWRXH8B"
}
```

**Response (Success - 200 OK):**
```json
{
  "name": "Apple AirPods Pro (2nd Generation) Wireless Ear Buds.. .",
  "price": 249.00,
  "currency": "USD",
  "url": "https://www.amazon.com/dp/B0CHWRXH8B",
  "retailer": "Amazon"
}
```

**Response (Error - 400 Bad Request):**
```json
{
  "detail": "Currently only Amazon URLs are supported"
}
```

**Response (Error - 500 Internal Server Error):**
```json
{
  "detail": "Scraping failed:  [error message]"
}
```

---

## 🧪 Testing

### Manual Testing with Postman

1. **Health Check:**
   ```
   GET http://localhost:8000/health
   ```

2. **Track Product:**
   ```
   POST http://localhost:8000/api/track
   Content-Type: application/json
   
   {
     "url":  "https://www.amazon.com/dp/B0CHWRXH8B"
   }
   ```

### Manual Testing with Frontend

1. Open **http://localhost:3000**
2.  Paste an Amazon product URL
3. Click **"Track Price"**
4. Verify product name, price, and currency display correctly

### Test Cases

| Test Case | URL | Expected Result |
|-----------|-----|-----------------|
| Valid Amazon. com (USD) | `https://www.amazon.com/dp/B0CHWRXH8B` | ✅ Product data with USD |
| Valid Amazon.co.uk (GBP) | `https://www.amazon.co.uk/dp/B0CHWRXH8B` | ✅ Product data with GBP |
| Valid Amazon.in (INR) | `https://www.amazon.in/dp/B0CHWRXH8B` | ✅ Product data with INR |
| Valid with LKR currency | Any Sri Lankan Amazon product | ✅ Product data with LKR |
| Invalid URL format | `not-a-url` | ❌ 422 Validation Error |
| Non-Amazon URL | `https://www.ebay.com/itm/123` | ❌ 400 Error |
| Mobile responsive | Test on mobile viewport | ✅ UI adapts correctly |

---

## 🌍 Supported Currencies

| Currency | Code | Symbol |
|----------|------|--------|
| US Dollar | USD | $ |
| Euro | EUR | € |
| British Pound | GBP | £ |
| Japanese Yen | JPY | ¥ |
| Indian Rupee | INR | ₹ |
| Sri Lankan Rupee | LKR | Rs.  |
| Australian Dollar | AUD | A$ |
| Canadian Dollar | CAD | C$ |
| Singapore Dollar | SGD | S$ |
| Malaysian Ringgit | MYR | RM |
| Philippine Peso | PHP | ₱ |
| Thai Baht | THB | ฿ |
| Brazilian Real | BRL | R$ |
| South African Rand | ZAR | R |
| Swedish Krona | SEK | kr |
| Polish Zloty | PLN | zł |
| UAE Dirham | AED | د.إ |
| Saudi Riyal | SAR | SR |

---

## 🔒 Environment Variables

### Backend (`backend/. env`)
```env
PORT=8000
ENVIRONMENT=development
```

### Frontend (`frontend/.env.local`)
```env
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

---

## 📝 Development Workflow

### Branch Strategy

```bash
# Create feature branch
git checkout -b feature/feature-name

# Develop and test locally
# ... 

# Commit changes
git add .
git commit -m "feat: description of feature"

# Push to GitHub
git push origin feature/feature-name

# Create Pull Request on GitHub
# After review, merge to main
```

### Commit Message Convention

Follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting)
- `refactor:` Code refactoring
- `test:` Adding tests
- `chore:` Maintenance tasks

---

## 🐛 Known Issues & Limitations

### Current Limitations
- ⚠️ **Amazon-only**:  Currently supports Amazon URLs only (not eBay, Walmart, etc.)
- ⚠️ **No persistence**: Product data not saved to database (in-memory only)
- ⚠️ **No authentication**: No user accounts or login system
- ⚠️ **No price history**: Cannot track price changes over time
- ⚠️ **Rate limiting**: Amazon may block requests if too many in short time

### Known Issues
- 🐛 Amazon occasionally changes HTML structure, breaking scraper
- 🐛 Some Amazon pages use different price selectors
- 🐛 Currency detection may need updates for new regions

### Workarounds
- If scraping fails, try a different Amazon product URL
- Refresh the page if getting rate-limited errors
- Use VPN if Amazon blocks your IP

---

## 🗺️ Roadmap

### Phase 1: Foundation (✅ Complete)
- [x] Basic Amazon scraping
- [x] Multi-currency support
- [x] Professional UI
- [x] RESTful API

### Phase 2: Persistence (🔄 Next)
- [ ] PostgreSQL database integration
- [ ] Product storage
- [ ] Price history tracking
- [ ] Database migrations

### Phase 3: User Features
- [ ] User authentication (JWT)
- [ ] User dashboard
- [ ] Watchlist management
- [ ] Price drop alerts

### Phase 4: Notifications
- [ ] Email notifications
- [ ] SMS notifications (Twilio)
- [ ] Webhook support
- [ ] Browser notifications

### Phase 5: Expansion
- [ ] Chrome extension
- [ ] Firefox extension
- [ ] Multi-retailer support (eBay, Walmart, Best Buy)
- [ ] Price comparison

### Phase 6: Advanced Features
- [ ] AI-powered price negotiation emails
- [ ] Automated negotiation
- [ ] Price prediction (ML)
- [ ] Mobile app (React Native)

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'feat: Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**manamendraJN**

- GitHub: [@manamendraJN](https://github.com/manamendraJN)

---

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [Next.js](https://nextjs.org/) - React framework for production
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) - Web scraping library
- [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS framework
- [Pydantic](https://docs.pydantic.dev/) - Data validation library

---

## 📞 Support

If you encounter any issues or have questions: 

1. Check the [Known Issues](#-known-issues--limitations) section
2. Search [existing issues](https://github.com/manamendraJN/pricefighter/issues)
3. Create a [new issue](https://github.com/manamendraJN/pricefighter/issues/new)

---

## ⭐ Show Your Support

Give a ⭐️ if this project helped you!

---

**Built with ❤️ for people who hate overpaying**