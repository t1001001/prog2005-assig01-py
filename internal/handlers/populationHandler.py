from fastapi import APIRouter, HTTPException, Query
import httpx
from typing import List, Optional
from internal.constants.constants import COUNTRIESNOW_API_URL
from internal.models.models import Population, PopulationValue

router = APIRouter()

# if there is no ISO2 code
@router.get("/population")
def default_population_handler():
    return {"message": "please type in an ISO2 code"}

# population handler to get information about the population of a country based on its ISO2 code
@router.get("/population/{iso_code}", response_model = Population)
async def populationHandler(iso_code: str, limit: Optional[str] = Query(None, description="Year range format: YYYY-YYYY")):

    if len(iso_code) != 2:
        raise HTTPException(status_code = 400, detail = "Invalid ISO2 code")
    
    iso_code = iso_code.upper()

    # parse year range
    start_year = end_year = None
    if limit:
        try:
            parts = limit.split("-")
            if len(parts) != 2:
                raise ValueError
            start_year = int(parts[0])
            end_year = int(parts[1])
        except:
            raise HTTPException(status_code = 400, detail = "Invalid limit format")
        
    # get country name from ISO2 code
    async with httpx.AsyncClient() as client:
        countriesnow_url = f"{COUNTRIESNOW_API_URL}countries/info?returns=iso2"
        try:
            countriesnow_resp = await client.get(countriesnow_url)
            countriesnow_resp.raise_for_status()
        except:
            raise HTTPException(status_code = 500, detail = "Error fetching country data")
        
        try:
            data = countriesnow_resp.json()["data"]
            country_name = next((c["name"] for c in data if c["iso2"].upper() == iso_code), None)
        except:
            raise HTTPException(status_code=500, detail="Failed to process country info")
    
        if not country_name:
            raise HTTPException(status_code=404, detail=f"No country found for ISO2 code {iso_code}")
        
        # fetch population data
        population_url = f"{COUNTRIESNOW_API_URL}countries/population"
        try:
            population_resp = await client.get(population_url)
            population_resp.raise_for_status()
        except:
            raise HTTPException(status_code=500, detail="Failed to fetch population data")

        try:
            population_data = population_resp.json()["data"]
        except:
            raise HTTPException(status_code=500, detail="Failed to process population data")

        country_data = next((c for c in population_data if c["country"].lower() == country_name.lower()), None)
        if not country_data:
            raise HTTPException(status_code=404, detail=f"Population data not found for {country_name}")

        values = []
        total = 0
        count = 0

        for entry in country_data["populationCounts"]:
            year = entry["year"]
            value = entry["value"]
            if ((start_year is None or year >= start_year) and
                (end_year is None or year <= end_year)):
                values.append(PopulationValue(year=year, value=value))
                total += value
                count += 1

        if count == 0:
            raise HTTPException(status_code=404, detail="No population data for given year range")

        mean = total // count

    return Population(country=country_name, mean=mean, values=values)