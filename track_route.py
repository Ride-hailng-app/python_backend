import requests
import base64

ACCOUNT_ID = "HpnYbs5tz4fhd_oAYQHIxcLvXlk"
SECRET_KEY = "11rNJqLL5wDrRyhmbIH2TVQeJiEObLx398EKHoB7aq_e-RMtOGsc6Q"

AUTHORIZATION_TOKEN = "Basic {}".format(
    base64.b64encode(f"{ACCOUNT_ID}:{SECRET_KEY}".encode("utf-8")).decode("utf-8")
)
AUTH_HEADER = {"Authorization": AUTHORIZATION_TOKEN}
dev_id	=	"544C4571-1DBA-4FF7-9D5A-DCB272ED1593"
main_order_data = {
   "track_mode": "on_time",
   "route_handle": "2d012f0f-d302-4a2a-a2c9-1127df66f256",
   "device_id": "00112233-4455-6677-8899-AABBCCDDEEFF"
}

order_data = {
   "track_mode": "on_time",
   "route_handle": "2d012f0f-d302-4a2a-a2c9-1127df66f256"
}

route = requests.post('https://v3.api.hypertrack.com/orders/track', json=order_data, headers=AUTH_HEADER)
print(route.json())