from fastapi import APIRouter, HTTPException, Query
import httpx
from internal.constants.constants import RESTCOUNTRIES_API_URL, COUNTRIESNOW_API_URL
from internal.models.models import Country

router = APIRouter()

# if there is no ISO2 code
@router.get("/info")
def default_info_handler():
    return {"message": "please type in an ISO2 code"}

# info handler to see information of a country based on its ISO2 code
@router.get("/info/{iso_code}", response_model = Country)
async def info_handler(iso_code: str, limit: int = Query(default = 10, description = "Limit number of cities")):
    if len(iso_code) != 2:
        raise HTTPException(status_code = 400, detail = "Invalid ISO2 code")
    
    iso_code = iso_code.upper()

    async with httpx.AsyncClient() as client:
        # fetch data from RESTCountries API
        restcountries_url = f"{RESTCOUNTRIES_API_URL}alpha/{iso_code}"
        try:
            restcountries_resp = await client.get(restcountries_url)
            restcountries_resp.raise_for_status()
        except:
            raise HTTPException(status_code = 500, detail = "Error fetching country data")
        
        restcountries_json = restcountries_resp.json()

        if not isinstance(restcountries_json, list) or not restcountries_json:
            raise HTTPException(status_code = 404, detail = "Country not found")
        
        country_data = restcountries_json[0]

        # fetch data from CountriesNow API
        countriesnow_url = f"{COUNTRIESNOW_API_URL}countries/info?returns=iso2,cities"
        try:
            countriesnow_resp = await client.get(countriesnow_url)
            countriesnow_resp.raise_for_status()
        except:
            raise HTTPException(status_code = 500, detail = "Error fetching city data")
        
        countriesnow_data = countriesnow_resp.json().get("data", [])
        cities = []

        for entry in countriesnow_data:
            if entry.get("iso2", "").upper() == iso_code:
                cities = entry.get("cities", [])
                break

        if limit > 0 and len(cities) > limit:
            cities = cities[:limit]

        # inject cities into the response model
        country_data["cities"] = cities

        # pydantic will parse nested structures for `name` and `flags`
        try:
            return Country(**country_data)
        except Exception as e:
            raise HTTPException(status_code = 500, detail="Invalid country data format")