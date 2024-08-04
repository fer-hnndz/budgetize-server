"""Budgetize API Routes"""

from google_auth_oauthlib.flow import Flow
from flask import redirect, request, url_for, session
from budgetize_server import app

# * ============== Drive ==================

SCOPES = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/drive.appdata",
]
REDIRECT_URI = "http://localhost:8080/oauthcallback"

flow = Flow.from_client_secrets_file(
    "credentials.json",
    scopes=SCOPES,
)
flow.redirect_uri = REDIRECT_URI

# Generate URL for request to Google's OAuth 2.0 server.
authorization_url, state = flow.authorization_url(
    access_type="offline",
    # Optional, enable incremental authorization. Recommended as a best practice.
    include_granted_scopes="true",
    login_hint="hint@example.com",
    prompt="select_account",
)


# * ============== Routes ==================
@app.route("/", methods=["GET", "POST"])
def index():
    """Index route"""

    print(request.headers)
    if request.method == "POST":
        return request.get_data()

    return {"message": "Hello, World!", "status": 200}


@app.route("/authorize", methods=["GET"])
def connect_drive():
    """Endpoint to connect to Google Drive"""
    return redirect(authorization_url)


@app.route("/oauthcallback", methods=["GET"])
def oauth_callback():
    return 200

    # TODO: Store credentials in session
    # auth_response = request.url
    # print("Auth Response: ", auth_response)
    # flow.fetch_token(authorization_url=auth_response)

    # creds = flow.credentials
    # session["credentials"] = {
    #     "token": creds.token,
    #     "refresh_token": creds.refresh_token,
    #     "token_uri": creds.token_uri,
    #     "client_id": creds.client_id,
    #     "client_secret": creds.client_secret,
    #     "scopes": creds.scopes,
    # }
    # return session
