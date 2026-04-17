import time
from fastapi import FastAPI, Depends, Request, APIRouter
from fastapi.responses import Response
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.middleware.cors import CORSMiddleware

from app.auth import verify_token
from app.services import get_market_data, generate_analysis_report

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address, default_limits=["10/minute"])

app = FastAPI(
    title="Trade Opportunities API",
    description="API for analyzing market data and providing trade opportunity insights.",
    version="1.0.0"
)

# Apply rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter()

@router.get("/analyze/{sector}")
@limiter.limit("5/minute")
def analyze_sector(
    request: Request,
    sector: str,
    token: str = Depends(verify_token)
):
    """
    Analyzes market data for a given sector.
    Requires guest token; rate limited to 5/minute.
    """
    context_data = get_market_data(sector)
    
    # gemini report
    markdown_report = generate_analysis_report(sector, context_data)
    
    # formatted markdown
    return Response(
        content=markdown_report, 
        media_type="text/markdown",
        headers={"Content-Disposition": f"attachment; filename=\"{sector}_market_analysis.md\""}
    )

app.include_router(router)

@app.get("/health")
def health_check():
    return {"status": "ok", "timestamp": time.time()}
