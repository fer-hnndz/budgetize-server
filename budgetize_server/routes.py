"""Budgetize API Routes"""

import json
import os
from datetime import timezone
from traceback import print_exc
from typing import TypedDict

import httpx
from arrow import Arrow
from flask import request

from budgetize_server import app


class LatestResponse(TypedDict):
    base: str
    date: str
    rates: dict[str, float]


CURRENCY_API_KEY = os.environ.get("CURRENCY_API_KEY")
LATEST_RESPONSE: LatestResponse = {}
VALID_RATE_TIME = 7 * 24 * 60 * 60  # 1 week in seconds


@app.route("/", methods=["GET", "POST"])
def index():
    """Index route"""

    if request.method == "POST":
        return request.get_data()

    return {"message": "Hello, World!", "status": 200}


def get_exchange(base: str, conversion: str):
    if not base in LATEST_RESPONSE["rates"]:
        return {"error": f"Base currency {base} not supported."}

    if not conversion in LATEST_RESPONSE["rates"]:
        return {"error": f"Conversion currency {conversion} not supported."}

    base_rate = LATEST_RESPONSE["rates"][base]
    conversion_rate = LATEST_RESPONSE["rates"][conversion]
    return conversion_rate / base_rate


@app.route("/currency/<string:base>/<string:conversion>")
def convert_currency(base: str, conversion: str):
    global LATEST_RESPONSE

    if LATEST_RESPONSE:
        return {"rate": get_exchange(base, conversion)}

    url = "https://api.exchangeratesapi.io/v1/latest"
    r = httpx.get(url, params={"access_key": CURRENCY_API_KEY})

    if r.status_code != 200:
        return {"error": "Could not retrieve exchange rates."}

    LATEST_RESPONSE = json.loads(r.text)
    return {"rate": get_exchange(base, conversion)}


# @app.route("/currency/<string:base>/<string:conversion>/<float:amount>")
# async def convert_currency(base: str, conversion: str, amount: float):
#     if base.upper() == conversion.upper():
#         return amount

#     if f"{base.upper()}-{conversion.upper()}" in retrieved_rates:
#         return retrieved_rates[f"{base.upper()}-{conversion.upper()}"]

#     try:
#         async with httpx.AsyncClient() as client:
#             url = f"https://www.xe.com/currencyconverter/convert/?Amount={amount}&From={base.upper()}&To={conversion.upper()}"
#             r = await client.get(url, timeout=8)

#             soup = BeautifulSoup(r.text, "html.parser")

#             main_element = soup.find("main")
#             if not main_element:
#                 raise Exception("Could not find main element in response html.")

#             digits_span = soup.find("span", class_="faded-digits")

#             if digits_span is None:
#                 raise Exception(
#                     "Could not scrape exchange rate. Please look at last_html_response.html in Budgetize's folder"
#                 )

#             digits_str: str = digits_span.get_text().replace(",", "")
#             parent_div = digits_span.parent  # type:ignore

#             # Get first element of the iterator
#             for child in parent_div.children:  # type:ignore
#                 rate_p = str(child).replace(",", "")
#                 break

#             amount_of_zero = len(rate_p.split(".")[-1])
#             digits_to_sum = ("0." + ("0" * amount_of_zero)) + digits_str
#             rate = float(rate_p) + float(digits_to_sum)

#             key = f"{base.upper()}-{conversion.upper()}"
#             now = Arrow.now(tzinfo=timezone.utc)
#             if not key in retrieved_rates:
#                 retrieved_rates[f"{base.upper()}-{conversion.upper()}"] = {
#                     "rate": rate,
#                     "retrieved_at": now.timestamp(),
#                 }
#             elif (
#                 now.timestamp()
#                 >= retrieved_rates[key]["retrieved_at"] + VALID_RATE_TIME
#             ):
#                 retrieved_rates[key] = {
#                     "rate": rate,
#                     "retrieved_at": now.timestamp(),
#                 }

#             return retrieved_rates[key]
#     except Exception as e:
#         print_exc()
#         print(r.text)
#         return "400"
