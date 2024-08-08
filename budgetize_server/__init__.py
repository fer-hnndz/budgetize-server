"""Budgetize's server module"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from budgetize_server.orm._base import Base

app = Flask(__name__)
db = SQLAlchemy(model_class=Base)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite"
db.init_app(app)

from budgetize_server import routes
from budgetize_server.orm.account import Account
from budgetize_server.orm.transactions import Transaction
from budgetize_server.orm.user import User

with app.app_context():
    db.create_all()
