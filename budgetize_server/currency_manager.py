import os

import arrow
import httpx
from arrow import Arrow

EXCHANGE_API_URL = "https://api.exchangeratesapi.io/v1/latest"


class CurrencyManager:
    rates: dict[str, float] = {}

    def __init__(self) -> None:
        self._MAX_AGE = 7 * 24 * 60 * 60

        self.date_fetched = Arrow.utcnow()
        self._get_latest_rates()

    def _check_expired_fetch(self) -> bool:
        """
        Checks if the current fetched rates are older than 1 week.
        """
        return (
            Arrow.utcnow().timestamp() - self.date_fetched.timestamp() >= self._MAX_AGE
        )

    def _get_latest_rates(self):
        """
        Fetches the latest exchange rates.
        """
        key = os.getenv("EXCHANGE_RATE_API_KEY")

        if not key:
            raise ValueError("EXCHANGE_RATE_API_KEY not set.")

        r = httpx.get(EXCHANGE_API_URL, params={"access_key": key})
        data = r.json()

        self.rates = data["rates"]
        self.date_fetched = Arrow.utcnow()

    def convert(self, base: str, conversion: str, amount: float) -> float:
        """
        Converts the base currency to the conversion currency.

        Args:
            base (str): The base currency.
            conversion (str): The currency to convert to.
        """

        if self._check_expired_fetch():
            self._get_latest_rates()

        base_rate = self.rates.get(base.upper())
        conversion_rate = self.rates.get(conversion.upper())

        if not base_rate or not conversion_rate:
            raise ValueError(f"{base} or {conversion} not supported.")

        return (amount / base_rate) * conversion_rate
