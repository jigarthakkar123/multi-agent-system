import json
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..core.security import get_current_user
from ..models.user import User
from ..services.kpi_calculator import KPICalculator
from ..core.config import settings
import httpx

router = APIRouter(prefix="/chat", tags=["AI Business Chat"])

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str
    source_metrics: dict

@router.post("", response_model=ChatResponse)
def ask_ai_chat(
    req: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    calculator = KPICalculator(db)
    kpis = calculator.get_summary_kpis()
    cities = calculator.get_city_performance()
    sources = calculator.get_lead_sources()
    expenses = calculator.get_category_expenses()
    
    question = req.message.strip().lower()
    
    # Grounded context
    context = (
        f"Real Estate Agency Performance Data (May 1 - Oct 31, 2026):\n"
        f"- Total Closed Won Sales Volume: ₹{kpis['total_revenue']:,.2f}\n"
        f"- Total Brokerage Commission Earned: ₹{kpis['total_commission']:,.2f}\n"
        f"- Total Operational Expenses: ₹{kpis['total_expenses']:,.2f}\n"
        f"- Net Profit: ₹{kpis['net_profit']:,.2f} (Margin: {kpis['profit_margin_pct']}%)\n"
        f"- Total Leads: {kpis['total_leads']}, Converted: {kpis['converted_leads']} ({kpis['conversion_rate_pct']}%)\n"
        f"- Closed Won Deals: {kpis['closed_won_deals']} of {kpis['total_deals']} ({kpis['deal_win_rate_pct']}%)\n"
        f"- Sold Properties: {kpis['sold_inventory_units']} of {kpis['total_inventory_units']} ({kpis['absorption_rate_pct']}%)\n"
        f"- Average Price per sqft: ₹{kpis['avg_property_price_sqft']:,.2f}/sqft\n"
        f"- Top City by Revenue: {cities[0]['city']} (₹{cities[0]['revenue_generated']:,.2f})\n"
        f"- Top Lead Source: {sources[0]['source']} ({sources[0]['conversion_rate']}% conversion rate)\n"
        f"- Largest Expense Category: {expenses[0]['category']} (₹{expenses[0]['amount']:,.2f})\n"
    )

    # 1. Try OpenAI if key is present
    if settings.OPENAI_API_KEY:
        try:
            url = "https://api.openai.com/v1/chat/completions"
            headers = {"Authorization": f"Bearer {settings.OPENAI_API_KEY}"}
            payload = {
                "model": "gpt-4o-mini",
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are the AI Business Operations & Decision Intelligence Assistant for a real estate agency. "
                            "Answer questions with professional precision using ONLY the ground-truth facts provided. "
                            f"Ground-Truth Telemetry:\n{context}"
                        )
                    },
                    {"role": "user", "content": req.message}
                ],
                "temperature": 0.2
            }
            resp = httpx.post(url, headers=headers, json=payload, timeout=20.0)
            if resp.status_code == 200:
                data = resp.json()
                reply_text = data["choices"][0]["message"]["content"].strip()
                return {"reply": reply_text, "source_metrics": kpis}
        except Exception:
            pass

    # 2. Try Gemini if key is present
    if settings.GEMINI_API_KEY:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={settings.GEMINI_API_KEY}"
            payload = {
                "contents": [{
                    "parts": [{
                        "text": f"You are an AI Business Decision Intelligence Assistant for a real estate agency. "
                                f"Answer accurately using ONLY this verified data:\n{context}\n\n"
                                f"User Question: {req.message}"
                    }]
                }]
            }
            resp = httpx.post(url, json=payload, timeout=15.0)
            if resp.status_code == 200:
                data = resp.json()
                reply_text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                return {"reply": reply_text, "source_metrics": kpis}
        except Exception:
            pass

    # 3. Deterministic factual fallback if no external LLM configured
    if "revenue" in question or "sales" in question or "volume" in question:
        reply = (
            f"Between May 1 and October 31, 2026, the agency generated a total closed sales volume of ₹{kpis['total_revenue']:,.2f} "
            f"across {kpis['closed_won_deals']} closed won deals. Total brokerage commissions earned reached ₹{kpis['total_commission']:,.2f}."
        )
    elif "profit" in question or "margin" in question:
        reply = (
            f"The agency achieved a net operating profit of ₹{kpis['net_profit']:,.2f} with a net operating profit margin of {kpis['profit_margin_pct']}%. "
            f"Total commissions earned were ₹{kpis['total_commission']:,.2f} against operational expenses of ₹{kpis['total_expenses']:,.2f}."
        )
    elif "city" in question or "mumbai" in question or "pune" in question or "where" in question:
        reply = (
            f"Geographic market analysis shows that {cities[0]['city']} is our highest-grossing market with ₹{cities[0]['revenue_generated']:,.2f} "
            f"in closed sales, followed by {cities[1]['city']} (₹{cities[1]['revenue_generated']:,.2f}) and {cities[2]['city']} (₹{cities[2]['revenue_generated']:,.2f})."
        )
    elif "lead" in question or "marketing" in question or "source" in question or "channel" in question:
        reply = (
            f"Out of {kpis['total_leads']} total inquiries, {kpis['converted_leads']} converted ({kpis['conversion_rate_pct']}%). "
            f"Our highest-converting channel is '{sources[0]['source']}' at {sources[0]['conversion_rate']}% conversion rate, "
            f"while walk-in and social media channels show high pre-qualification dropout."
        )
    elif "expense" in question or "cost" in question or "spending" in question:
        reply = (
            f"Total operational expenses were ₹{kpis['total_expenses']:,.2f}. The largest single expense category was "
            f"'{expenses[0]['category']}' at ₹{expenses[0]['amount']:,.2f} ({expenses[0]['percentage']}%), followed by "
            f"'{expenses[1]['category']}' at ₹{expenses[1]['amount']:,.2f}."
        )
    elif "strategy" in question or "recommend" in question or "action" in question:
        reply = (
            f"The Strategy Agent recommends three prioritized actions: 1) Reallocating ₹45,00,000 to high-ROI digital property portals; "
            f"2) Deploying automated sub-2hr site visit dispatching; 3) Repricing slow-moving warehouse inventory in Bharuch/Anand. "
            f"All actions are currently staged in the Human-in-the-Loop Approval Queue."
        )
    else:
        reply = (
            f"Based on our May–October 2026 real estate dataset: Total revenue is ₹{kpis['total_revenue']:,.2f}, "
            f"net operating profit is ₹{kpis['net_profit']:,.2f} ({kpis['profit_margin_pct']}% margin), overall lead conversion rate is {kpis['conversion_rate_pct']}%, "
            f"and property inventory absorption is {kpis['absorption_rate_pct']}%. Let me know if you would like deeper details on specific cities, channels, or expenses."
        )
        
    return {"reply": reply, "source_metrics": kpis}
