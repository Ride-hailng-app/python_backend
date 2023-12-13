import requests
import base64

ACCOUNT_ID = "HpnYbs5tz4fhd_oAYQHIxcLvXlk"
SECRET_KEY = "11rNJqLL5wDrRyhmbIH2TVQeJiEObLx398EKHoB7aq_e-RMtOGsc6Q"

AUTHORIZATION_TOKEN = "Basic {}".format(
    base64.b64encode(f"{ACCOUNT_ID}:{SECRET_KEY}".encode("utf-8")).decode("utf-8")
)
AUTH_HEADER = {"Authorization": AUTHORIZATION_TOKEN}

main_order_data = {
  "device_id": "00112233-4455-6677-8899-AABBCCDDEEFF",
  "track_mode": "on_time",
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
      "scheduled_at": "2023-03-14T23:30:00Z",
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
      "metadata": {"customerId": "2233321"},
    },
  ]
}


order_data = {
  "device_id": "AB039A71-FD25-4584-A29C-61CE712C5B3E",
  "track_mode": "on_time",
  "orders": [
    {
      "order_handle": "walk_man_order-112238",
      
      
      "destination": {
        "geometry": {
          "type": "Point",
          "coordinates": [32.562928, 0.350260]
        },
        "radius": 50
      },
      "product_type": ["walker"],
      "capacity_used": 1,
      "expected_service_time": 800,
      "type": "drop",
      "metadata": {"customerId": "2233322"},
    }
  ]
}



route = requests.post('https://v3.api.hypertrack.com/orders/track', json=order_data, headers=AUTH_HEADER)
print(route.json())