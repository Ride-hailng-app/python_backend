import requests
import base64
 

ACCOUNT_ID = "HpnYbs5tz4fhd_oAYQHIxcLvXlk"
SECRET_KEY = "11rNJqLL5wDrRyhmbIH2TVQeJiEObLx398EKHoB7aq_e-RMtOGsc6Q"
#dev_id = "001FA236-3678-480E-A6BE-E5DFB54F71EE"
dev_id	=	"544C4571-1DBA-4FF7-9D5A-DCB272ED1593"

AUTHORIZATION_TOKEN = "Basic {}".format(
    base64.b64encode(f"{ACCOUNT_ID}:{SECRET_KEY}".encode("utf-8")).decode("utf-8")
)
print(AUTHORIZATION_TOKEN)
AUTH_HEADER = {"Authorization": AUTHORIZATION_TOKEN}

driver_data2 = {
   "device_id":"001FA236-3678-480E-A6BE-E5DFB54F71EE",
   "ops_group_handle":"5c5a43a0-19ef-4b96-9539-8ab6c4e4238a",
   "driver_handle":"test1-driver-1_marksman",
   "name": "Max man",
   "home":{
      "address":"Finca Kawempe Branch, Bombo Road, Kazo Angola, Kawempe, Kampala Capital City, Kampala, Wakiso, Central Region, Uganda",
      "geometry":{
         "coordinates":[
            32.562578,
            0.358502
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
         "end_time": "00:00",
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
   }
}


driver_data = {
   
   "device_id":"001FA236-3678-480E-A6BE-E5DFB54F71EE",
   "driver_handle":"test1-driver-1_marksman",
   "name": "Max man",
   "product_types":[
      "Food"
   ]
}

#response = requests.post("https://v3.api.hypertrack.com/drivers",
#json=driver_data,auth=("{ACCOUNT_ID}", "{SECRET_KEY}"))
#
response = requests.post("https://v3.api.hypertrack.com/drivers",
json=driver_data,headers=AUTH_HEADER)
#auth=("{AccountId}", "{SecretKey}")
print(response)

