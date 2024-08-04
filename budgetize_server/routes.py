"""Budgetize API Routes"""

from budgetize_server import app

# SERVICE = build("drive", "v3")


@app.route("/")
def index():
    """Index route"""
    return {"message": "Hello, World!", "status": 200}


@app.route("/v1/connect", methods=["GET"])
def connect_drive():
    """Endpoint to connect to Google Drive"""
    return 200
