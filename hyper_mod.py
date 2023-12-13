import requests
import base64,uuid
from hypertrack.rest import Client
from hypertrack.exceptions import HyperTrackException
from constants import *

AUTHORIZATION_TOKEN = "Basic {}".format(
    base64.b64encode(f"{ACCOUNT_ID}:{SECRET_KEY}".encode("utf-8")).decode("utf-8")
)
print(AUTHORIZATION_TOKEN)
AUTH_HEADER = {"Authorization": AUTHORIZATION_TOKEN}

winstons_tag = "fx_winston_driver"
hypertrack = Client(ACCOUNT_ID,SECRET_KEY)
def gen_driver_handle(driva_contact):
    return base64.b64encode(driva_contact.encode("utf-8"))
def create_driver(dri_id,dev_id,dri_name):
    #driv_name = dri_name.replace(" ","_")

    driver_handle = "fx_winston_driver_"+dri_id
    driver_data = {
        "device_id":dev_id,
        "driver_handle":driver_handle,
        "name": dri_name,
        "profile":
        {
         "gig_type":"rider_man"
        },
        "product_types":[
                            "People"
                         ]
    }

    response = requests.post("https://v3.api.hypertrack.com/drivers",
    json=driver_data,headers=AUTH_HEADER)
    print(response.status_code)
    print(response.json())
    return response.status_code

def update_driver(dri_id,dev_id):
    driver_handle = "fx_winston_driver_"+dri_id

    driver_data = {
        "device_id":dev_id,
        "profile":
        {
         "gig_type":"rider_man"
        }
    }

    response = requests.patch(f"https://v3.api.hypertrack.com/drivers/{driver_handle}",
    json=driver_data,
    headers=AUTH_HEADER)
    print(response.json())
    return response.status_code

def kill_order(ord_hwd):
        response = requests.post(f"https://v3.api.hypertrack.com/orders/{ord_hwd}/complete",
                                headers=AUTH_HEADER)
        return response
def del_driver(dri_id):
    driver_handle = "fx_winston_driver_"+dri_id
    response = requests.delete(f"https://v3.api.hypertrack.com/drivers/{driver_handle}",headers=AUTH_HEADER)
    print(response.status_code)
#winston_ride_order_fx_winston_driver_702891117
def gen_device_map(dev_id):
    return f"https://embed.hypertrack.com/tracking/{dev_id}?publishable_key={publishable_key}"
    #print(response.json())

def get_nearby(coord_lon,coord_lat):
    payload = {
                "order":{
                "destination":{
                            "geometry":
                                    {
                                     "coordinates":[coord_lon,coord_lat],
                                     "type":"Point"
                                    }
                              }
                        },
                        "search_filter":{
      "driver_profile":{
         "user_type":"rider_fx"
      }},
                 "search_type":"region"
                }

    response = requests.request("POST", "https://v3.api.hypertrack.com/nearby/v3", json = payload,headers=AUTH_HEADER)
    print("old one : ",response.json())
    #response = {'drivers': [{'device': {'device_id': '82F1F305-407E-41E4-8985-A81EDFC83F0C', 'info': {'timezone': 'Africa/Kampala', 'os_name': 'Android', 'device_brand': 'Sony', 'sdk_version': '6.4.2', 'device_model': 'SOV36', 'network_operator': 'AIRTEL UGANDA', 'name': None, 'os_version': '9', 'os_hardware_identifier': '9393ce616c8c504d'}, 'profile': None, 'status': {'value': 'active', 'data': {'activity': 'stop', 'recorded_at': '2023-09-06T02:20:41.353Z'}}}, 'location': {'geometry': {'type': 'Point', 'coordinates': [32.563039, 0.358858]}}, 'duration': None, 'distance': 179.09294773648384, 'ongoing_trip': None, 'error': None}], 'summary': {'total_drivers': 1, 'processed_drivers': 1, 'unprocessed_drivers': 0, 'outside_region_drivers': 0, 'no_route_drivers': 0}}
    #print(f"new {response}")
    return(response.json())

def get_nearby_rider(coord_lon,coord_lat):
    payload = {
                "order":{
                "destination":{
                            "geometry":
                                    {
                                     "coordinates":[coord_lon,coord_lat],
                                     "type":"Point"
                                    }
                              }
                        },
                 "search_type":"region",
                 "search_filter":{
      "driver_profile":{
         "gig_type":"rider_man"
      },
      "include_on_trip":True,
                }
    }
                



    #response = requests.request("POST", "https://v3.api.hypertrack.com/nearby/v3", json = payload,headers=AUTH_HEADER)
    #print(response)
    response = requests.request("POST", "https://v3.api.hypertrack.com/nearby/v3", json = payload,headers=AUTH_HEADER)
    print("old one : ",response.json())
    response = {'drivers': [{'device': {'device_id': '82F1F305-407E-41E4-8985-A81EDFC83F0C', 'info': {'timezone': 'Africa/Kampala', 'os_name': 'Android', 'device_brand': 'Sony', 'sdk_version': '6.4.2', 'device_model': 'SOV36', 'network_operator': 'AIRTEL UGANDA', 'name': None, 'os_version': '9', 'os_hardware_identifier': '9393ce616c8c504d'}, 'profile': None, 'status': {'value': 'active', 'data': {'activity': 'stop', 'recorded_at': '2023-09-06T02:20:41.353Z'}}}, 'location': {'geometry': {'type': 'Point', 'coordinates': [32.563039, 0.358858]}}, 'duration': None, 'distance': 179.09294773648384, 'ongoing_trip': None, 'error': None}], 'summary': {'total_drivers': 1, 'processed_drivers': 1, 'unprocessed_drivers': 0, 'outside_region_drivers': 0, 'no_route_drivers': 0}}
    print(f"new {response}")
    return(response)
    #print(response.json())
    #response = {'drivers': [], 'summary': {'total_drivers': 0, 'processed_drivers': 0, 'unprocessed_drivers': 0, 'outside_region_drivers': 0, 'no_route_drivers': 0}}
    #response = {'drivers': [{'device': {'device_id': 'D6D603A7-6F8C-43AB-886D-5100D4F290B4', 'info': {'timezone': 'Africa/Kampala', 'os_name': 'Android', 'device_brand': 'Sony', 'sdk_version': '6.4.2', 'device_model': 'SOV36', 'network_operator': 'AIRTEL UGANDA', 'name': None, 'os_version': '9', 'os_hardware_identifier': '9393ce616c8c504d'}, 'profile': None, 'status': {'value': 'active', 'data': {'activity': 'stop', 'recorded_at': '2023-09-06T02:20:41.353Z'}}}, 'location': {'geometry': {'type': 'Point', 'coordinates': [32.563039, 0.358858]}}, 'duration': None, 'distance': 179.09294773648384, 'ongoing_trip': None, 'error': None}], 'summary': {'total_drivers': 1, 'processed_drivers': 1, 'unprocessed_drivers': 0, 'outside_region_drivers': 0, 'no_route_drivers': 0}}
    return response

def del_device(dev_id):
    del_stat = hypertrack.devices.delete(dev_id)
    return del_stat

def set_driver_status(dev_handle,driva_stat):
        print(f"using dev handle: {dev_handle}")
        driver_data = {"tracking": driva_stat,"available": driva_stat}
        response = requests.post(f"https://v3.api.hypertrack.com/drivers/{dev_handle}/work_status",
                json=driver_data,
                headers=AUTH_HEADER)
        return response

def set_dev_name(dev_id,dev_name):
    set_stat = hypertrack.devices.change_name(dev_id,dev_name)
    return set_stat

def gen_order(u_id,olon,olat):
    order_data = {
                "plan_mode": "manual",
                "ops_group_handle": "store_berkx",
                "orders": [
                {
                    "order_handle": f"order-{u_id}",
                    "scheduled_at": "2023-09-02T09:00:00Z",
                    "destination": {
                            "geometry": {
                                            "type": "Point",
                                            "coordinates": [olon,olat]
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
    return route

def gen_walk_order(u_id,olon,olat):
    order_data = {
                    "device_id": u_id,
                    "track_mode": "on_time",
                    "orders": [
                                {
                                    "order_handle": f"winston_walker_order_{u_id}",
                                    "destination": {
                                                      "geometry": {
                                                                    "type": "Point",
                                                                    "coordinates": [olon, olat]
                                                                },
                                                      "radius": 50
                                                    },
                                     "product_type": ["walker"],
                                     "capacity_used": 1,
                                     "expected_service_time": 800,
                                     "type": "drop",
                                     "metadata": {"customerId": u_id},
                                }
                              ]
                 }
    route = requests.post('https://v3.api.hypertrack.com/orders/track', json=order_data, headers=AUTH_HEADER)
    #print(route.json())
    return route

def gen_ride_order(xu_id,olon,olat):
    u_id = "fx_winston_driver_"+xu_id
    order_data = {
                    "driver_handle": u_id,
                    "track_mode": "on_time",
                    "orders": [
                                {
                                    "order_handle": f"winston_ride_order_{u_id}"+str(uuid.uuid4()),
                                    "destination": {
                                                      "geometry": {
                                                                    "type": "Point",
                                                                    "coordinates": [olon, olat]
                                                                },
                                                      "radius": 50
                                                    },
                                     "product_type": ["walker"],
                                     "capacity_used": 1,
                                     "expected_service_time": 800,
                                     "type": "drop",
                                     "metadata": {"customerId": u_id},
                                }
                              ]
                 }
    route = requests.post('https://v3.api.hypertrack.com/orders/track', json=order_data, headers=AUTH_HEADER)
    print(route.json())
    return route

def complete_order(order_handle):
    response = requests.post(f"https://v3.api.hypertrack.com/orders/{order_handle}/complete",
                                headers=AUTH_HEADER)
    return response

def cancel_order(order_handle):
    response = requests.post(f"https://v3.api.hypertrack.com/orders/{order_handle}/cancel",
                                headers=AUTH_HEADER)
    return response
#response = requests.request("POST", "https://v3.api.hypertrack.com/nearby/v3", data=json.dumps(payload).encode("utf-8"),headers=AUTH_HEADER)
#auth=("{AccountId}", "{SecretKey}"))


#del_driver("test1-driver-1_marksman")
#create_driver("test1-driver-1_marksman",'','Test Man')
#print(get_nearby(32.562578,0.358502))

#cancel_order("winston_walker_order_A74E0416-71FB-49A3-A470-9AE5ADF2E3C4")
#get_nearby(32.562733, 0.35905)