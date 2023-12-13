import requests
import base64

ACCOUNT_ID = "HpnYbs5tz4fhd_oAYQHIxcLvXlk"
SECRET_KEY = "11rNJqLL5wDrRyhmbIH2TVQeJiEObLx398EKHoB7aq_e-RMtOGsc6Q"

AUTHORIZATION_TOKEN = "Basic {}".format(
    base64.b64encode(f"{ACCOUNT_ID}:{SECRET_KEY}".encode("utf-8")).decode("utf-8")
)
AUTH_HEADER = {"Authorization": AUTHORIZATION_TOKEN}

main_ops_group_data = {
   "ops_group_handle":"store_berk",
   "ops_group_label": "Store",
   "route_start_location": "ops_group_home",
   "route_completion_type": "end_at_last_order",
    "ops_group_home": {
      "geometry":{
         "coordinates":[
            32.562928, 0.350260
         ],
         "type":"Point"
      },
      "address":"Store Berkley address"
    },
    "objective_fn": "minimise_time",
    "route_capacity": 10,
    "route_max_distance": 12000,
    "default_shift_start_time": "07:00",
    "default_shift_end_time": "18:00",
    "timezone": "America/Los Angeles"
}

ops_group_data = {
   "ops_group_handle":"store_berkx",
   "ops_group_label": "Storex",
   "route_start_location": "ops_group_home",
   "route_completion_type": "end_at_last_order",
    "ops_group_home": {
      "geometry":{
         "coordinates":[
            32.562928, 0.350260
         ],
         "type":"Point"
      },
      "address":"Store Berkley address"
    }
}

response = requests.post("https://v3.api.hypertrack.com/ops-groups",
json=ops_group_data,
headers=AUTH_HEADER)
print(response.json())