import json
import os
from pathlib import Path

import arrow
import httpx
from arrow import Arrow

EXCHANGE_API_URL = "https://api.exchangeratesapi.io/v1/latest"


class CurrencyManager:
    rates: dict[str, float] = {}

    def __init__(self) -> None:
        self._MAX_AGE = 7 * 24 * 60 * 60  # 1 week in seconds
        self._data_file = Path(__file__).resolve().parent / "exchange_rates.json"
        self.date_fetched = Arrow.utcnow()
        self._load_or_update_rates()

    def _is_data_expired(self) -> bool:
        """
        Checks if the current fetched rates are older than 1 week.
        """
        return (
            Arrow.utcnow().timestamp() - self.date_fetched.timestamp() >= self._MAX_AGE
        )

    def _fetch_latest_rates(self):
        """
        Fetches the latest exchange rates from the API and saves them to the file.
        """
        print("[CurrencyManager] Fetching currencies from API....")
        key = os.getenv("EXCHANGE_RATE_API_KEY")

        if not key:
            raise ValueError("EXCHANGE_RATE_API_KEY not set.")

        r = httpx.get(EXCHANGE_API_URL, params={"access_key": key})
        if r.status_code != 200:
            raise ConnectionError("Failed to fetch exchange rates from the API.")

        data = r.json()
        self.rates = data["rates"]
        self.date_fetched = Arrow.utcnow()

        self._save_rates_to_file()

    def _save_rates_to_file(self):
        """
        Saves the fetched exchange rates and timestamp to a file.
        """
        with self._data_file.open("w", encoding="utf-8") as f:
            json.dump(
                {"rates": self.rates, "date_fetched": self.date_fetched.isoformat()}, f
            )

    def _load_or_update_rates(self):
        """
        Loads the exchange rates from the file or fetches them if the file doesn't exist
        or the data is expired.
        """
        if self._data_file.exists():
            with self._data_file.open("r", encoding="utf-8") as f:
                data = json.load(f)
                self.rates = data.get("rates", {})
                self.date_fetched = arrow.get(data.get("date_fetched", ""))

                print("[CurrencyManager] Loaded currencies from file.")

            if not self.rates or self._is_data_expired():
                print("[CurrencyManager] Fetching latest rates... (expired or empty)")
                self._fetch_latest_rates()
        else:
            print("[CurrencyManager] Fetching latest rates... (file not found)")
            self._fetch_latest_rates()

    def convert(self, base: str, conversion: str, amount: float) -> float:
        """
        Converts the base currency to the conversion currency.

        Args:
            base (str): The base currency.
            conversion (str): The currency to convert to.
            amount (float): The amount to convert.

        Returns:
            float: The converted amount.
        """
        if self._is_data_expired():
            self._fetch_latest_rates()

        base_rate = self.rates.get(base.upper())
        conversion_rate = self.rates.get(conversion.upper())

        if not base_rate or not conversion_rate:
            raise ValueError(f"{base} or {conversion} not supported.")

        return (amount / base_rate) * conversion_rate
