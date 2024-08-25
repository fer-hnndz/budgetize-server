"""Budgetize's server module"""

from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

load_dotenv()
app = Flask(__name__)

from budgetize_server import routes
