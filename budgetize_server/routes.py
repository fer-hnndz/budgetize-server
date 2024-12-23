"""Budgetize API Routes"""

import json
from typing import TypedDict

import httpx
from arrow import Arrow
from flask import request

from budgetize_server import app


class LatestResponse(TypedDict):
    base: str
    date: str
    rates: dict[str, float]


LATEST_RESPONSE: LatestResponse = {}
VALID_RATE_TIME = 7 * 24 * 60 * 60  # 1 week in seconds


@app.route("/", methods=["GET", "POST"])
def index():
    """Index route"""

    if request.method == "POST":
        return request.get_data()

    return {"message": "Hello, World!", "status": 200}


def _get_exchange(base: str, conversion: str):
    if not base.upper() in LATEST_RESPONSE["rates"]:
        return {"error": f"Base currency {base} not supported."}

    if not conversion.upper() in LATEST_RESPONSE["rates"]:
        return {"error": f"Conversion currency {conversion} not supported."}

    base_rate = LATEST_RESPONSE["rates"][base.upper()]
    conversion_rate = LATEST_RESPONSE["rates"][conversion.upper()]
    return conversion_rate / base_rate


@app.route("/currency/<string:base>/<string:conversion>")
def convert_currency(base: str, conversion: str):
    """Converts the base currency to the conversion currency"""

    global LATEST_RESPONSE

    if LATEST_RESPONSE:
        return {"rate": _get_exchange(base, conversion)}

    key = app.config["EXCHANGE_API_KEY"]
    print("Requesting with key: ", key)

    url = "https://api.exchangeratesapi.io/v1/latest"
    r = httpx.get(url, params={"access_key": key})
    if r.status_code != 200:
        return {"error": "Could not retrieve exchange rates."}

    LATEST_RESPONSE = json.loads(r.text)
    return {"rate": _get_exchange(base, conversion)}
