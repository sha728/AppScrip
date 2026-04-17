# Trade Opportunities API

A FastAPI service that analyzes market data and provides trade opportunity insights for specific sectors in India, using DuckDuckGo Search and Google Gemini LLM.

## Setup Instructions

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file from the example:
   ```bash
   cp .env.example .env
   ```
   Add your `GEMINI_API_KEY` to the `.env` file. You can also customize `GUEST_AUTH_TOKEN`.

3. Run the development server:
   ```bash
   uvicorn app.main:app --reload
   ```

## Usage

The API is protected. Include your `GUEST_AUTH_TOKEN` in the `Authorization` header as a Bearer token.
By default, the token is `secret_guest_token`.

Endpoint: `GET /analyze/{sector}`

### Example Request
```bash
curl -H "Authorization: Bearer secret_guest_token" http://localhost:8000/analyze/pharmaceuticals
```
