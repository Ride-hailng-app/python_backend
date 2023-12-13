import requests
import base64
AUTHORIZATION_TOKEN = "Basic {}".format(
    base64.b64encode(f"{ACCOUNT_ID}:{SECRET_KEY}".encode("utf-8")).decode("utf-8")
)
AUTH_HEADER = {"Authorization": AUTHORIZATION_TOKEN}

response = requests.delete("https://v3.api.hypertrack.com/drivers/test-driver-1",
headers=AUTH_HEADER)