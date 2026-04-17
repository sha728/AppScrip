# Trade Opportunities API 🚀

Hey! This is a small FastAPI service I built to analyze market data and find trade opportunities for specific business sectors in India. It pulls live context from the web (using DuckDuckGo) and feeds it right into the Google Gemini API to generate a nice, structured markdown report for you. 

## Getting Started

To get this running locally, just follow these quick steps:

1. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up the config:**
   Copy the example environment file to create your own:
   ```bash
   cp .env.example .env
   ```
   Then, open up that new `.env` file and drop in your `GEMINI_API_KEY`. You can also change the `GUEST_AUTH_TOKEN` to whatever secret password you want to use to protect the API.

3. **Spin up the server:**
   ```bash
   uvicorn app.main:app --reload
   ```

## How to use it

Because the API is protected, you'll need to pass your guest token as a Bearer token in the request header. 

The absolutely easiest way to test it is to pop open `http://localhost:8000/docs` in your browser while the server is running. Click the little lock icon 🔒 at the top right, enter your token (defaults to `secret_guest_token`), and give the `GET /analyze/{sector}` endpoint a spin!

If you're more of a terminal person, here's a standard cURL example:
```bash
curl -H "Authorization: Bearer secret_guest_token" http://localhost:8000/analyze/pharmaceuticals
```
