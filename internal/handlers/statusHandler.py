from fastapi import APIRouter
import httpx
from internal.constants.constants import VERSION, RESTCOUNTRIES_API_URL, COUNTRIESNOW_API_URL
from internal.models.models import Status
import time

router = APIRouter()

start_time = time.time()

# sends a HEAD request to the endpoints to see if theyre available
async def check_status(base_url: str) -> str:
    if "v3.1" in base_url:
        status_url = base_url + "all"
    elif "v0.1" in base_url:
        status_url = base_url + "countries"
    else:
        status_url = base_url

    try: 
        async with httpx.AsyncClient() as client:
            resp = await client.head(status_url)
            if resp.status_code == 200:
                return "Available"
    except httpx.RequestError as exc:
        return "Unavailable"
    
# status handler to see the status of the API
@router.get("/status", response_model = Status)
async def status_handler():

    status = Status(
        countriesNowAPI = await check_status(COUNTRIESNOW_API_URL),
        restCountriesAPI = await check_status(RESTCOUNTRIES_API_URL),
        version = VERSION,
        uptime = int(time.time() - start_time)
    )

    return status