from fastapi import APIRouter
from typing import TypedDict, Optional
import json
import httpx

router = APIRouter(prefix="/currency", tags=["currency"])


class LatestResponse(TypedDict):
    base: str
    date: str
    rates: dict[str, float]


EXCHANGE_API_URL = "https://api.exchangeratesapi.io/v1/latest"
LATEST_RESPONSE: LatestResponse = {"base": "", "date": "", "rates": {}}
VALID_RATE_TIME = 7 * 24 * 60 * 60  # 1 week in seconds


async def _get_exchange(base: str, conversion: str):
    if (
        not base.upper() in LATEST_RESPONSE["rates"]
        or not conversion.upper() in LATEST_RESPONSE["rates"]
    ):
        return {"error": f"{base} or {conversion} not supported."}

    base_rate = LATEST_RESPONSE["rates"][base.upper()]
    conversion_rate = LATEST_RESPONSE["rates"][conversion.upper()]
    return conversion_rate / base_rate


@router.get("/")
async def index():
    """Returns all available currencies"""
    return "200"


@router.get("/{base}/")
async def currencies_base(base: str):
    """Returns the exchange rate for all currencies based on the base currency"""

    global LATEST_RESPONSE

    if LATEST_RESPONSE:
        return {
            await _get_exchange(base, currency) for currency in LATEST_RESPONSE["rates"]
        }

    key = "the key goes here"

    r = httpx.get(EXCHANGE_API_URL, params={"access_key": key})

    if r.status_code != 200:
        return {"error": "Could not retrieve exchange rates."}

    LATEST_RESPONSE = json.loads(r.text)

    return {
        await _get_exchange(base, currency) for currency in LATEST_RESPONSE["rates"]
    }

    return "200"
