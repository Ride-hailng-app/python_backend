import requests
import base64


ACCOUNT_ID = "HpnYbs5tz4fhd_oAYQHIxcLvXlk"
SECRET_KEY = "11rNJqLL5wDrRyhmbIH2TVQeJiEObLx398EKHoB7aq_e-RMtOGsc6Q"
#dev_id = "001FA236-3678-480E-A6BE-E5DFB54F71EE"
dev_id	=	"544C4571-1DBA-4FF7-9D5A-DCB272ED1593"

AUTHORIZATION_TOKEN = "Basic {}".format(
    base64.b64encode(f"{ACCOUNT_ID}:{SECRET_KEY}".encode("utf-8")).decode("utf-8")
)
AUTH_HEADER = {"Authorization": AUTHORIZATION_TOKEN}

response = requests.get("https://v3.api.hypertrack.com/drivers/test1-driver-1_marksman/history",
headers=AUTH_HEADER)

print(response.json())