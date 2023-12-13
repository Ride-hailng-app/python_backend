import requests
import base64

ACCOUNT_ID = "HpnYbs5tz4fhd_oAYQHIxcLvXlk"
SECRET_KEY = "11rNJqLL5wDrRyhmbIH2TVQeJiEObLx398EKHoB7aq_e-RMtOGsc6Q"
AUTHORIZATION_TOKEN = "Basic {}".format(
    base64.b64encode(f"{ACCOUNT_ID}:{SECRET_KEY}".encode("utf-8")).decode("utf-8")
)
AUTH_HEADER = {"Authorization": AUTHORIZATION_TOKEN}


#res ="{'ops_group_handle': 'store_berkx', 'ops_group_label': 'Storex', 'route_start_location': 'ops_group_home', 'route_completion_type': 'end_at_last_order', 'shift_availability_mode': 'manual', 'order_tracking_mode': 'manual', 'timezone': 'UTC', 'ops_group_home': {'geometry': {'type': 'Point', 'coordinates': [32.562928, 0.35026]}, 'address': 'Store Berkley address'}}"

main_order_data = {
  "plan_mode": "scheduled",
  "ops_group_handle": "store_berkx",
  "orders": [
    {
      "order_handle": "order-112233",
      "scheduled_after": "2023-03-14T22:00:00Z",
      "scheduled_at": "2023-03-14T23:00:00Z",
      "destination": {
        "geometry": {
          "type": "Point",
          "coordinates": [-122.398096, 37.793038]
        },
        "radius": 50
      },
      "product_type": ["plumber"],
      "capacity_used": 1,
      "expected_service_time": 800,
      "type": "drop",
      "metadata": {"customerId": "2233322"},
    },
    {
      "order_handle": "order-112244",
      "scheduled_after": "2023-03-14T23:00:00Z",
      "scheduled_at": "2023-09-14T23:30:00Z",
      "destination": {
        "address": "425 Montgomery Street, San Francisco, CA 94108, United States",
        "radius": 50
      },
      "product_type": ["plumber"],
      "capacity_used": 1,
      "expected_service_time": 800,
      "type": "drop",
      "metadata": {"customerId": "2233321"},
    },
  ]
}

order_data = {
  "plan_mode": "manual",
   "driver_handle": "fx_winston_driver_fxpro6cf645d7-fdca-4d83-b335-9b50bbe8d942",
   "ops_group_handle": "store_berkx",
  "orders": [
    {
      "order_handle": "order-112233xp",
      "scheduled_at": "2023-09-30T08:40:00Z",
      "destination": {
        "geometry": {
          "type": "Point",
          "coordinates": [32.562928, 0.350260]
        },
        "radius": 50
      },
      "product_type": ["rider"],
      "capacity_used": 1,
      "expected_service_time": 800,
      "type": "drop",
      "metadata": {"customerId": "2233322"},
    }
  ]
}


route = requests.post('https://v3.api.hypertrack.com/orders', json=order_data, headers=AUTH_HEADER)

print(route.json())