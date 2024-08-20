"""Budgetize API Routes"""

from flask import redirect, request
from google_auth_oauthlib.flow import Flow

from budgetize_server import app, db
from budgetize_server.orm.user import User
import asyncio
import httpx
from bs4 import BeautifulSoup
from arrow import Arrow
from datetime import timezone

VALID_RATE_TIME = 7 * 24 * 60 * 60  # 1 week in seconds
retrieved_rates = {}


@app.route("/", methods=["GET", "POST"])
def index():
    """Index route"""

    if request.method == "POST":
        return request.get_data()

    return {"message": "Hello, World!", "status": 200}


@app.route("/currency/<string:base>/<string:conversion>/<float:amount>")
async def convert_currency(base: str, conversion: str, amount: float):
    if base.upper() == conversion.upper():
        return amount

    if f"{base.upper()}-{conversion.upper()}" in retrieved_rates:
        return retrieved_rates[f"{base.upper()}-{conversion.upper()}"]

    try:
        async with httpx.AsyncClient() as client:
            url = f"https://www.xe.com/currencyconverter/convert/?Amount={amount}&From={base.upper()}&To={conversion.upper()}"
            r = await client.get(url, timeout=8)

            soup = BeautifulSoup(r.text, "html.parser")

            main_element = soup.find("main")
            if not main_element:
                raise Exception("Could not find main element in response html.")

            digits_span = soup.find("span", class_="faded-digits")

            if digits_span is None:
                raise Exception(
                    "Could not scrape exchange rate. Please look at last_html_response.html in Budgetize's folder"
                )

            digits_str: str = digits_span.get_text().replace(",", "")
            parent_div = digits_span.parent  # type:ignore

            # Get first element of the iterator
            for child in parent_div.children:  # type:ignore
                rate_p = str(child).replace(",", "")
                break

            amount_of_zero = len(rate_p.split(".")[-1])
            digits_to_sum = ("0." + ("0" * amount_of_zero)) + digits_str
            rate = float(rate_p) + float(digits_to_sum)

            key = f"{base.upper()}-{conversion.upper()}"
            now = Arrow.now(tzinfo=timezone.utc)
            if not key in retrieved_rates:
                retrieved_rates[f"{base.upper()}-{conversion.upper()}"] = {
                    "rate": rate,
                    "retrieved_at": now.timestamp(),
                }
            elif (
                now.timestamp()
                >= retrieved_rates[key]["retrieved_at"] + VALID_RATE_TIME
            ):
                retrieved_rates[key] = {
                    "rate": rate,
                    "retrieved_at": now.timestamp(),
                }

            return retrieved_rates[key]
    except Exception as e:
        print(e)
        return "400"
