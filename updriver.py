import requests
import base64
AUTHORIZATION_TOKEN = "Basic {}".format(
    base64.b64encode(f"{ACCOUNT_ID}:{SECRET_KEY}".encode("utf-8")).decode("utf-8")
)
AUTH_HEADER = {"Authorization": AUTHORIZATION_TOKEN}

driver_data = {
   "device_id":"BB898EC6-63A9-4E60-97E1-D1042F8CDF33",
   "name": "Om Shah",
   "ops_group_handle":"5c5a43a0-19ef-4b96-9539-8ab6c4e4238a",
   "home":{
      "address":"123 Street, Koramangala, Bangalore, Karnataka, India, 560034",
      "geometry":{
         "coordinates":[
            77.61119269564921,
            12.93458618334973
         ],
         "type":"Point"
      }
   },
   "product_types":[
      "Food"
   ],
   "schedule":[
      {
         "start_time": "07:00",
         "end_time": "12:00",
         "date": "2023-04-04"
      },
      {
         "start_time": "04:00",
         "end_time": "18:00",
         "date": "2023-04-04"
      }
   ],
   "profile":{
      "name":"Test Driver A"
   },
   "unavailable_on": ["2023-06-06"]
}

response = requests.patch("https://v3.api.hypertrack.com/drivers/test-driver-1",
json=driver_data,
headers=AUTH_HEADER)

print(response)