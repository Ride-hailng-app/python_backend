import firebase_admin
from firebase_admin import credentials, messaging
import json,index
from constants import *
cred = credentials.Certificate("serviceKey.json")
firebase_admin.initialize_app(cred)


def test():
        
        or_data={
                "order_id": "8b282bd3-5117-11ee-8a35-f0def1115cf6",
                "order_details":{
                "customer_name":"Winston 256",
                "customer_contact":"070289007",
                "customer_coords":[0.360419,32.562005]
                                }  # Your JSON data here
                 }
        index.addOrderJ(or_data)
        jor_data = json.dumps(or_data)
        print(f"json string:  {jor_data}")
        message = messaging.Message(
                                        data={"message":jor_data,"cmd":"order_200"},
                                        token=client_token,
                                        notification={
                                                title: "Weather Warning!",
                                                body: "A new weather warning has been issued for your location.",
                                                imageUrl: "https://my-cdn.com/extreme-weather.png",
                                                }
                                    )

        # Send the message
        response = messaging.send(message)
        print(f"sent data and response is: ")

def ping(client_token,or_data,cmd):
        print(f"using client token {client_token}")
        jor_data = json.dumps(or_data)
        print(f"json string:  {jor_data}")
        message = messaging.Message(
                                        data={"message":jor_data,"cmd":cmd},
                                        token=client_token,
                                    )

        # Send the message
        response = messaging.send(message)
        print(f"sent data and response is: ")