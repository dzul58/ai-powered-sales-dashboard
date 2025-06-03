# AI-Powered Sales Dashboard

## Overview

A modern full-stack application featuring a sales dashboard with AI capabilities using:

1. **Next.js** as the frontend framework
2. **FastAPI** as the backend API
3. **Redis** for caching
4. **Google Gemini AI** for sales data analysis
5. **Docker** for containerization and microservices

## Tech Stack

- **Frontend**: Next.js, React, TailwindCSS
- **Backend**: FastAPI, Python 3.11
- **Database/Cache**: Redis
- **AI**: Google Gemini API
- **Container**: Docker & Docker Compose
- **Environment**: Python-dotenv

## Features

1. **Sales Dashboard**

   - Sales representative data visualization
   - Filtering by name, role, region, and skills
   - Pagination for large datasets
   - Redis caching for better performance

2. **AI-Powered Analysis**

   - Google Gemini AI integration
   - Natural language sales data analysis
   - AI response caching
   - Rich context for accurate analysis

3. **Microservices Architecture**
   - Separate services for frontend, backend, and Redis
   - Docker containerization
   - Environment variables configuration
   - CORS security configuration

## Setup & Installation

### Prerequisites

- Docker & Docker Compose
- Google Cloud Account (for Gemini API key)
- Git

### Installation Steps

1. **Clone Repository**

   ```bash
   git clone https://github.com/<your-username>/ai-powered-sales-dashboard.git
   cd ai-powered-sales-dashboard
   ```

2. **Setup Environment Variables**
   Create a `.env` file in the `backend` folder with the following content:

   ```env
   # API Configuration
   HOST=0.0.0.0
   PORT=8000

   # Redis Configuration
   REDIS_HOST=redis
   REDIS_PORT=6379
   REDIS_DB=0

   # CORS Configuration
   CORS_ORIGINS=["http://localhost:3000"]

   # Cache Duration (in seconds)
   SALES_CACHE_DURATION=300
   AI_CACHE_DURATION=600

   # Gemini AI Configuration
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

3. **Run with Docker**

   ```bash
   # Build and run all services
   docker-compose up --build

   # Run in background
   docker-compose up -d

   # View logs
   docker-compose logs -f
   ```

4. **Access the Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Redis: localhost:6379

### Project Structure

```
.
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py
│   └── .env
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   └── ...
├── dummyData.json
└── docker-compose.yml
```

## Usage

### API Endpoints

1. **Sales Data**

   ```bash
   # Get all sales representatives
   GET http://localhost:8000/api/sales-reps

   # With filters
   GET http://localhost:8000/api/sales-reps?name=alice&region=North%20America

   # With pagination
   GET http://localhost:8000/api/sales-reps?page=1&page_size=10
   ```

2. **AI Analysis**

   ```bash
   # Analyze data with AI
   POST http://localhost:8000/api/ai
   Content-Type: application/json

   {
     "question": "Who is the sales representative with the highest total deal value?"
   }
   ```

### AI Features

- Natural language queries
- Complex analysis support
- Example questions:
  - "What is the total value of Closed Won deals?"
  - "Who is the best performing sales rep in the Asia region?"
  - "What are the sales trends by region?"
  - "Compare sales rep performance based on their skills"

## Development

### Local Development (without Docker)

1. **Backend**

   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # or `venv\Scripts\activate` on Windows
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

2. **Frontend**

   ```bash
   cd frontend
   npm install
   npm run dev
   ```

3. **Redis**

   ```bash
   # Install Redis based on OS
   # MacOS
   brew install redis
   brew services start redis

   # Ubuntu
   sudo apt-get install redis-server
   sudo systemctl start redis
   ```

### Best Practices

1. **Environment Variables**

   - Never commit `.env` files to repository
   - Use `.env.example` as a template
   - Always validate environment variables at startup

2. **Caching**

   - Use Redis for caching frequently accessed data
   - Set appropriate TTL (Time To Live)
   - Monitor cache hit/miss ratio

3. **Security**
   - Always use HTTPS in production
   - Validate input on backend
   - Implement rate limiting
   - Keep API keys secure

## Troubleshooting

### Common Issues

1. **Redis Connection Error**

   - Ensure Redis service is running
   - Check Redis environment variables
   - Verify Docker network

2. **Gemini API Error**

   - Validate API key
   - Check quota and rate limits
   - Ensure correct request format

3. **CORS Issues**
   - Verify CORS_ORIGINS in .env
   - Ensure frontend URL matches
   - Check browser console for error details
