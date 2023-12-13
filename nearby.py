import requests,json,base64

ACCOUNT_ID = "HpnYbs5tz4fhd_oAYQHIxcLvXlk"
SECRET_KEY = "11rNJqLL5wDrRyhmbIH2TVQeJiEObLx398EKHoB7aq_e-RMtOGsc6Q"

AUTHORIZATION_TOKEN = "Basic {}".format(
    base64.b64encode(f"{ACCOUNT_ID}:{SECRET_KEY}".encode("utf-8")).decode("utf-8")
)
AUTH_HEADER = {"Authorization": AUTHORIZATION_TOKEN}

payload = {
   "order":{
      "destination":{
         "geometry":{
            "coordinates":[
               32.562578,
            0.358502
            ],
            "type":"Point"
         }
      }
   },
   "search_type":"region"
}



response = requests.request("POST", "https://v3.api.hypertrack.com/nearby/v3", json = payload,headers=AUTH_HEADER)

#response = requests.request("POST", "https://v3.api.hypertrack.com/nearby/v3", data=json.dumps(payload).encode("utf-8"),headers=AUTH_HEADER)
#auth=("{AccountId}", "{SecretKey}"))

print(response.json())

