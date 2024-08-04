from flask import Flask

app = Flask(__name__)

from budgetize_server import routes
