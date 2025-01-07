import json
import os
from typing import Optional, TypedDict

import arrow
import httpx
from fastapi import APIRouter, HTTPException

from budgetize_server.currency_manager import CurrencyManager

router = APIRouter(prefix="/currency", tags=["currency"])
mgr = CurrencyManager()


@router.get("/")
async def index():
    """Returns all available currencies"""
    # Get an exchange to updatein case needed

    return mgr.rates


# @router.get("/{base}/")
# async def currencies_base(base: str):
#     """Returns the exchange rate for all currencies based on the base currency"""

#     global LATEST_RESPONSE

#     if LATEST_RESPONSE:
#         return {
#             await _get_exchange(base, currency) for currency in LATEST_RESPONSE["rates"]
#         }

#     return {
#         await _get_exchange(base, currency) for currency in LATEST_RESPONSE["rates"]
#     }

#     return "200"
