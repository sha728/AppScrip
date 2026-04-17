import logging
from duckduckgo_search import DDGS
import google.generativeai as genai
from app.models import settings

# Configure logging
logger = logging.getLogger("app.services")

# Configure Gemini
if settings.gemini_api_key:
    genai.configure(api_key=settings.gemini_api_key)

def get_market_data(sector: str) -> str:
    query = f"{sector} sector market trends opportunities India"
    logger.info(f"Searching for: {query}")
    
    try:
        ddgs = DDGS()
        results = list(ddgs.text(query, max_results=10))
        
        if not results:
            return "No recent market data found."
            
        context = ""
        for i, res in enumerate(results):
            context += f"Source {i+1}:\nTitle: {res.get('title')}\nSummary: {res.get('body')}\n\n"
        
        return context
    except Exception as e:
        logger.error(f"Error fetching market data: {e}")
        return f"Error retrieving market data: {str(e)}"

def generate_analysis_report(sector: str, context: str) -> str:
    if not settings.gemini_api_key:
        return f"# Analysis for {sector.title()} Sector\n\n**Warning:** Gemini API key is not configured. Please add `GEMINI_API_KEY` to the `.env` file.\n\n## Market Data Context\n\n{context}"
        
    prompt = f"""
You are an expert market analyst focusing on the Indian economy.

Please generate a structured, professional markdown report analyzing the trade and market opportunities for the '{sector}' sector in India.

Use the following recent market news and data context to inform your report:
<context>
{context}
</context>

Your report MUST be in Markdown format, using appropriate headings, bullet points, and structures. 
It should include at least the following sections:
1. Executive Summary
2. Current Market Trends
3. Key Trade Opportunities
4. Challenges & Risks
5. Strategic Recommendations

Only output the markdown content. Do not wrap it in markdown block quotes (```markdown), just the raw markdown tags.
"""
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        logger.info(f"Generating Gemini report for {sector}")
        response = model.generate_content(prompt)
        return response.text.replace("```markdown", "").replace("```", "")
    except Exception as e:
        logger.error(f"Error generating Gemini response: {e}")
        return f"# Analysis for {sector.title()} Sector\n\n## Error\n\nAn error occurred while generating the AI report: {str(e)}\n\n## Market Data Context\n\n{context}"
