from flask import request, url_for, jsonify, make_response
from budgetize_server import app


@app.route("/")
def index():
    return {"message": "Hello, World!", "status": 200}
