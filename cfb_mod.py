import firebase_admin, json
from firebase_admin import credentials, messaging
#farbiMz_Rs2K040wL-Wq22:APA91bEQwknA8GaihExuoFzZ9OBSxa6x2UBYGsD4GFU0uEolCOJ8ZegcuphmmdtEzbEfgt9lslKYCBHaVNzYaSLTFl71TQ-CNVxHx3w7UVPwa-K3D0vyVTNIkuAs6KgGKOqVn507ttrU&order=8b282bd3-5117-11ee-8a35-f0def1115cf6
creds = credentials.Certificate("serviceKey.json")
firebase_admin.initialize_app(creds)
client_token = "farbiMz_Rs2K040wL-Wq22:APA91bEQwknA8GaihExuoFzZ9OBSxa6x2UBYGsD4GFU0uEolCOJ8ZegcuphmmdtEzbEfgt9lslKYCBHaVNzYaSLTFl71TQ-CNVxHx3w7UVPwa-K3D0vyVTNIkuAs6KgGKOqVn507ttrU"

or_data={
        "order_id": "8b282bd3-5117-11ee-8a35-f0def1115cf6",
        "order_details":{
        "rider_name":"Winston 256",
        "rider_contact":"070289007",
        "rider_track": "https://track.me",
        #"customer_coords":[0.360419,32.562005]
        }  # Your JSON data here
    }

#index.addOrderJ(or_data)
jor_data = json.dumps(or_data)
print(f"json string:  {jor_data}")

fb_msg = messaging.Message(
    data={"message":jor_data,"cmd":"order_200"},
    token=client_token,
)


sent_res = messaging.send(fb_msg)
print("firrebase data sent: sent_res")

