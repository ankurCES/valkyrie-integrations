from fastapi import FastAPI
import httpx
import json
import os

app = FastAPI(title="Valkyrie-Integrations (Hermes)", version="0.1.0")

# Enterprise Mocks
MOCK_DATA = {
    "hr": {"status": "operational", "employees": 1250, "avg_tenure": "4.2 years"},
    "finance": {"quarterly_revenue": "$12.5M", "burn_rate": "$1.1M", "runway": "14 months"},
    "crm": {"active_leads": 450, "conversion_rate": "12.5%", "top_region": "North America"}
}

@app.get("/")
async def root():
    return {"message": "Hermes is standing ready. The message is true."}

@app.get("/weather")
async def get_weather(lat: float = 30.2672, lon: float = -97.7431):
    """Fetch public weather data via Open-Meteo."""
    async with httpx.AsyncClient() as client:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        response = await client.get(url)
        return response.json()

@app.get("/finance/market")
async def get_market_mock():
    """Simulate finance data integration."""
    return {"index": "GUNGNIR-500", "value": 4200.67, "change": "+1.2%"}

@app.get("/enterprise/{sector}")
async def get_enterprise_mock(sector: str):
    """Return local enterprise mocks (HR, Finance, CRM)."""
    return MOCK_DATA.get(sector.lower(), {"error": "Sector not found"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
