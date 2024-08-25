"""Budgetize's server module"""

import os

from dotenv import find_dotenv, load_dotenv
from flask import Flask

load_dotenv()
app = Flask(__name__)
app.config["EXCHANGE_API_KEY"] = os.getenv("EXCHANGE_RATE_API_KEY")

from budgetize_server import routes
