from fastapi import FastAPI, HTTPException, Cookie,WebSocket
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uuid
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import HTMLResponse,RedirectResponse
import starlette.status as status
from fastapi.responses import JSONResponse
import uuid,math,json
import mysql.connector
import dist_tools
import hyper_mod
import fb_mod

DATABASE_URL = "mysql+mysqlconnector://aye:aye@192.168.1.152/wevuuge"
#INSERT INTO hyperorders(ORDER_ID,DEV_ID,DRIVER_ID) VALUES (UUID(),'3885B450-E3D9-4932-8FB1-B4D93988F5F7','D6D603A7-6F8C-43AB-886D-5100D4F290B4')
users = dict()
rider_ws = dict()
user_ws = dict()
cooky_dic = dict()
#engine = create_engine(DATABASE_URL)

#config = {
#    "host": "sql.freedb.tech",
#    "user": "freedb_aye256",
#    "password": "#kfTH#mv7u?*TvZ",
#    "database": "freedb_wevuuge"
#}
#"host": "192.168.43.122",
#"host": "192.168.1.152",
config = {
    #"host": "192.168.43.122",
    
    #"host": "mysql5049.site4now.net",
    "host": "192.168.1.152",
    
    "user": "root",
    #"user": "a9f12d_wevuge",
    
    "password": "",
    #"password": "SQLalg0zDB",
    "database": "wevuuge"
    #"database": "db_a9f12d_wevuge"
}


#SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Base = declarative_base()

app = FastAPI()
conn = mysql.connector.connect(**config)
#static_obj = app.mount("/",StaticFiles(directory="templates"),"static")

page = Jinja2Templates(directory="templates")
#UPDATE `riders` SET `Rider_Status`='0' WHERE 'Rider_Name' = 'maxy';
#UPDATE `users` SET User_Lon='0',User_Lat='0' WHERE Names = 'Avan';
#using limit of 100 km
def addOrderJ(json_da):
    oid = json_da["order_id"]
    xjson_da = json.dumps(json_da)
    sx_txt = f"INSERT INTO hyperorders(ORDER_ID,DEV_ID,DRIVER_ID,ORDER_DATA) VALUES('{oid}','F149C7BA-EBFB-4B72-B48A-369F55ABD653','17B36E1E-352F-4348-8BEE-517D315C9D00','{xjson_da}')"
    sql_man = conn.cursor()
    sql_man.execute(sx_txt)
    conn.commit()
    #lsx_txt = f"SELECT ORDER_DATA FROM hyperorders WHERE DEV_ID='F149C7BA-EBFB-4B72-B48A-369F55ABD653'"
    #sql_man.execute(lsx_txt)
    #sqdta = sql_man.fetchall();
    #print(sqdta)
    #sj = json.loads(sqdta[0][0])
    #print(sj["msg"])

def findRider(uuid=str(),user_coords=dict()):
    lat = float(user_coords["latitude"])
    lon = float(user_coords["longitude"])
    print(f"\n\ncoordinates {lat} and {lon}")
    east_limit_lat, east_limit_lon = dist_tools.move_point_east(lat,lon,0.1)
    print(f"\\n\neast limit {east_limit_lat} and {east_limit_lon}")
    west_limit_lat, west_limit_lon = dist_tools.move_point_west(lat,lon,0.1)

    north_limit_lat, north_limit_lon = dist_tools.move_point_north(lat,lon,0.1)

    south_limit_lat, south_limit_lon = dist_tools.move_point_south(lat,lon,0.1)
    
    sql_txt = f"SELECT * FROM `riders` WHERE ((Rider_Lon<='{east_limit_lon}' OR Rider_Lon<='{west_limit_lon}' OR Rider_Lon<='{north_limit_lon}' OR Rider_Lon<='{south_limit_lon}') AND (Rider_Lat <='{east_limit_lat}' OR Rider_Lat <='{west_limit_lat}' OR Rider_Lat <='{north_limit_lat}' OR Rider_Lat <='{south_limit_lat}')) AND Rider_Status='1'"

    sql_man = conn.cursor()
    sql_man.execute(sql_txt)
    datax = sql_man.fetchall()
    rider_list = list()
    rider_lon_lats = list()
    rider_id_lists = list()
    near_riders = None
    print(datax)
    if len(datax)>0:
        for datumx in datax:
            if datumx[1] in rider_ws:
                rider_id_lists.append(datumx[1])
                rider_lon_lats.append((float(datumx[6]),float(datumx[5])))
                print(f"riders stuple {rider_lon_lats}")
                near_riders = dist_tools.find_nearest_coordinates_kdtree((lat,lon),rider_lon_lats,rider_id_lists,1)

        return  near_riders
    else:
        return None
def getUserData(cuuid=str()):
    print("getting user")
    sql_txt = f"SELECT Names,User_Contact FROM users WHERE UUID='{cuuid}'"
    usr_cursor = conn.cursor()
    usr_cursor.execute(sql_txt)

    data = usr_cursor.fetchall()
    usr_data = None
    if len(data)>0:
        usr_data = data[0]
    usr_cursor.close()
    return usr_data

def delRide(dev_id=str()):
    db_ctrl = conn.cursor()
    sql_txt = f"DELETE FROM hyperorders WHERE DEV_ID = '{dev_id}'"# AND ORDER_ID = '{order_id}'"
    print(f"deleting {sql_txt}")
    db_ctrl.execute(sql_txt)
    conn.commit()
    print("deleted")

def delOrder(order_id=str(),order_hnd=str()):
    order_status = hyper_mod.cancel_order(order_hnd)
    print("delete status: ",order_status)
    if order_status.status_code == 200:
        db_ctrl = conn.cursor()
        sql_txt = f"DELETE FROM hyperorders WHERE ORDER_ID = '{order_id}'"
        print(f"deleting {sql_txt}")
        db_ctrl.execute(sql_txt)
        conn.commit()
    
    print("deleted")


def riderOrderCtrl(order_id=str(),dev_id=str(),cursor=str(),order_cmd=int()):
    db_ctrl = conn.cursor()
    order_dta = {}
    if (order_cmd==200):
        sql_txt = f"SELECT DEV_ID,ORDER_DATA FROM hyperorders WHERE DRIVER_ID = '{dev_id}' AND ORDER_ID = '{order_id}'"
        db_ctrl.execute(sql_txt)

        udev_ids = db_ctrl.fetchall()
        print(udev_ids)
        if len(udev_ids)>0:
            udev_id = udev_ids[0][0]
            order_datum = json.loads(udev_ids[0][1]) 
            print(f"using udev id {udev_id} and order {order_datum}")
            usql_txt = f"SELECT FB_ID FROM app_users WHERE DEVICE_ID = '{udev_id}' UNION SELECT CONTACT FROM app_users WHERE DEVICE_ID = '{dev_id}'"
            db_ctrl.execute(usql_txt)

            ufb_ids = db_ctrl.fetchall()
            print(f"q data {ufb_ids}")
            if(len(ufb_ids)>0):
                #for ufb_id in ufb_ids:
                ufb_id = ufb_ids[0][0]
                tokdriver = ufb_ids[1][0]
                print(f"found fd id {ufb_id} and token {tokdriver}")
                d_coords = order_datum["order_src"]
                #["order_details"]["customer_coords"]
                
                rorder = hyper_mod.gen_ride_order(tokdriver,d_coords[1],d_coords[0])
                jorder = rorder.json()
                #jorder = {'route_handle': 'c962b015-c338-4386-bea7-cf2b7766b51c', 'status': 'tracking', 'version': 1, 'embed_url': 'https://embed.hypertrack.com/trips/c962b015-c338-4386-bea7-cf2b7766b51c?publishable_key=n7HizHArPLQKNdZAFUwLrlID2CoZw1WSwsN5qKidiiFhGL5uZg3nRU_K7RdNswcGbcLcASsBj6LvwAH7_UZG9A', 'orders': [{'order_handle': 'winston_ride_order_fx_winston_driver_702891117', 'fulfillment_attempt': 2, 'status': 'ongoing', 'destination': {'geometry': {'type': 'Point', 'coordinates': [32.5932808, 0.3008523]}, 'address': 'Cavendish University, Ggaba Road, Kabalagala, Makindye, Kampala Capital City, Kampala, Central Region, Uganda', 'radius': 50}, 'track_mode': 'on_time', 'started_at': '2023-09-17T13:43:02.577Z', 'type': 'drop', 'type_index': 0, 'expected_service_time': 800, 'capacity_used': 1, 'metadata': {'customerId': 'fx_winston_driver_702891117'}, 'region': {'country': 'Uganda', 'city': 'Kampala Capital City', 'state': 'Central Region'}, 'product_type': ['walker'], 'share_url': 'https://trck.at/Pvm0MZr4nE', 'device_id': '82F1F305-407E-41E4-8985-A81EDFC83F0C', 'driver_handle': 'fx_winston_driver_702891117', 'created_at': '2023-09-17T13:43:00.369Z', 'assigned_at': '2023-09-17T13:43:01.212Z', 'route_handle': 'c962b015-c338-4386-bea7-cf2b7766b51c', 'planned_at': '2023-09-17T13:43:00.369Z'}], 'started_at': '2023-09-17T13:43:02.173Z', 'assigned_at': '2023-09-17T13:43:01.264Z', 'created_at': '2023-09-17T13:43:00.502Z', 'device_id': '82F1F305-407E-41E4-8985-A81EDFC83F0C', 'driver_handle': 'fx_winston_driver_702891117', 'region': {'country': 'Uganda', 'city': 'Kampala Capital City', 'state': 'Central Region'}, 'planned_at': '2023-09-17T13:43:00.502Z'}
                print("\n\n\nreceived order: ",jorder)
                track_url = jorder['orders'][0]['share_url']
                order_dta = {"order_id":order_id,"track_point":track_url+"?icon=bike"}
                fb_mod.ping(ufb_id,order_dta,"order_cmd")

        else:
            print(f"no users right now for dev id {dev_id} and order_id {order_id}")

    elif (order_cmd == 400):
         sql_txt = f"DELETE FROM hyperorders WHERE DRIVER_ID = '{dev_id}' AND ORDER_ID = '{order_id}'"
         print(f"deleting {sql_txt}")
         db_ctrl.execute(sql_txt)
         conn.commit()
         print("deleted")

    db_ctrl.close()
    return order_dta



def getHyperRiders(cooky_str=str()):
    sql_txt = f"SELECT ORDER_HANDLE,DRIVER_ID FROM hyperorders WHERE DEV_ID='{cooky_str}'"
    usr_cursor = conn.cursor()
    usr_cursor.execute(sql_txt)

    data = usr_cursor.fetchall()
    usr_data = None
    if len(data)>0:
        usr_data = data[0]
    usr_cursor.close()
    return usr_data

def getRiderData(cuuid=str()):
    print("getting user")
    sql_txt = f"SELECT Rider_Name,Rider_Contact FROM riders WHERE UUID='{cuuid}'"
    usr_cursor = conn.cursor()
    usr_cursor.execute(sql_txt)

    data = usr_cursor.fetchall()
    usr_data = None
    print(f"rider  obtained {data}")
    if len(data)>0:
        usr_data = data[0]
    usr_cursor.close()
    print(f"rider  obtained {usr_data}")
    return usr_data



def matchRider(cuuid=str()):
    order_sql = conn.cursor()
    user_sql_txt = f"SELECT Rider_Name,Rider_Contact,Rider_Lon,Rider_Lat,order_id FROM riders WHERE UUID = '{cuuid}'"
    order_sql.execute(user_sql_txt)
    usr_details = order_sql.fetchall()[0]

    usr_data = dict()
    usr_data["names"] = usr_details[0]
    usr_data["telno"] = usr_details[1]
    usr_data["lon"] = usr_details[2]
    usr_data["lat"] = usr_details[3]
    usr_data["order_id"] = usr_details[4]
    

    sql_txt = f"SELECT customer_id FROM orders WHERE rider_id='{cuuid}' AND order_status='order_pending'"

    order_sql = conn.cursor()
    order_sql.execute(sql_txt)
    datum = order_sql.fetchall()[0]
    got_rider_id = datum[0]
    print(f"obtained user: {got_rider_id}")
    usr_data["user_id"] = got_rider_id

    return usr_data


def matchUser(cuuid=str()):
    order_sql = conn.cursor()
    user_sql_txt = f"SELECT NAMES,User_Contact,User_Lon,User_Lat,order_id FROM users WHERE UUID = '{cuuid}'"
    order_sql.execute(user_sql_txt)
    usr_details = order_sql.fetchall()[0]

    usr_data = dict()
    usr_data["names"] = usr_details[0]
    usr_data["telno"] = usr_details[1]
    usr_data["lon"] = usr_details[2]
    usr_data["lat"] = usr_details[3]
    usr_data["order_id"] = usr_details[4]
    

    sql_txt = f"SELECT rider_id FROM orders WHERE customer_id='{cuuid}' AND order_status='order_pending'"

    order_sql = conn.cursor()
    order_sql.execute(sql_txt)
    datum = order_sql.fetchall()[0]
    got_rider_id = datum[0]
    usr_data["rider_id"] = got_rider_id

    return usr_data

def addOrder(cuuid=str(),ruuid=str(),order_dic=None):
    print(order_dic)
    c_id = cuuid
    r_id = ruuid
    price = 5000
    start_lat = order_dic["latitude"]
    start_lon = order_dic["longitude"]
    end_lat = order_dic["to_latitude"]
    end_lon = order_dic["to_latitude"]
    order_stat = "order_pending"
    distance = 5
    order_man= conn.cursor()

    sql_update = f"UPDATE orders SET customer_id='{c_id}',rider_id='{r_id}',price='{price}',start_lat='{start_lat}',start_lon='{start_lon}',end_lat='{end_lat}',end_lon='{end_lon}',order_status='{order_stat}',distance='{distance}' WHERE customer_id='{c_id}' AND rider_id='{r_id}'"

    

    sql_txtx = f"INSERT INTO `orders`(`customer_id`,`rider_id`,`price`,`start_lat`,`start_lon`,`end_lat`,`end_lon`, `order_status`,`distance`) VALUES ('{c_id}','{r_id}','{price}','{start_lat}','{start_lon}','{end_lat}','{end_lon}','{order_stat}','{distance}')"
    
    sql_txt   =f"INSERT INTO orders(customer_id,rider_id,price,start_lat,start_lon,end_lat,end_lon,order_status,distance) VALUES ('{c_id}','{r_id}','{price}','{start_lat}','{start_lon}','{end_lat}','{end_lon}','{order_stat}','{distance}')"

    sql_order_id = f"SELECT order_id FROM orders WHERE (customer_id='{c_id}' AND rider_id='{r_id}') AND order_status='{order_stat}'"

    sql_kill_txt =f"UPDATE riders SET order_id=NULL WHERE UUID='{r_id}'"

    order_man.execute(sql_kill_txt)
    conn.commit()


   


    
    order_man.execute(sql_order_id)
    #conn.commit()

    xgot_order_ids = (order_man.fetchall())
    
    
    print(xgot_order_ids)
    got_order_id = None
    if len(xgot_order_ids) >0:
        o_id = xgot_order_ids[0]
        print(f"deleting order: {o_id}")
        sql_del = f"DELETE FROM orders WHERE order_id = '{o_id}'"
        order_man.execute(sql_del)
        conn.commit()

        #order_man.execute(sql_order_id)
         #conn.commit()

        #got_order_ids = (order_man.fetchall())[0]

        #got_order_id = got_order_ids[0]

        #sql_up_txt = f"UPDATE riders SET order_id='{got_order_id}' WHERE UUID='{r_id}'"
        #order_man= conn.cursor()
        #order_man.execute(sql_up_txt)
        #conn.commit()
    #else:
    
    order_man.execute(sql_txt)
    conn.commit()

    order_man.execute(sql_order_id)
         #conn.commit()

    got_order_ids = (order_man.fetchall())[0]

    got_order_id = got_order_ids[0]

    sql_up_txt = f"UPDATE riders SET order_id='{got_order_id}' WHERE UUID='{r_id}'"
    order_man= conn.cursor()
    order_man.execute(sql_up_txt)
    conn.commit()
    


    order_man.close()


@app.post("/riderStat")
async def riderStat(request: Request):
    rider_json = await request.json()
    cook_guy = await request.cookies.get("guy_cook")
    cook_type = request.cookies.get("guy_type")

@app.websocket("/approve")
async def approveOrder(websocket: WebSocket):
    print("receieveed web socket")
    await websocket.accept()
    while True:
        datax = await websocket.receive_text()
        print(f"data is {datax}")
        data = json.loads(datax)
        print(f"json  is {data}")
        if "guy_cmd" in data.keys():
            cmd = data["guy_cmd"]
            guy_cook = "fxpro"+data["guy_cook"]
            if guy_cook!=None:
                if data["guy_type"] == "rider":
                    if cmd == "start_scan":
                        print("scan started")
                        rider_ws[guy_cook] = websocket
                    elif cmd == "approve_order":
                        usr_id = matchRider(guy_cook)
                        print(f"approving user : {usr_id}")
                        
                        if usr_id['user_id'] in user_ws.keys():
                            rider_data = getRiderData(guy_cook)
                            rider_ws_json = {}
                            rider_ws_json["name"] = rider_data[0]
                            rider_ws_json["tel"] = rider_data[1]

                            print(f"sending rider data {rider_ws_json}")

                            await user_ws[usr_id['user_id']].send_text(json.dumps(rider_ws_json))
                            print("order approved")
                        else:
                            print("\nerror, no user")
                    else:
                        print("no more commands")
                    print("ono rider")
                elif data["guy_type"] == "customer":
                    print("ono customer")
                    if cmd == "match_user":
                        print(" user scan started")
                        user_ws[guy_cook] = websocket
                    elif cmd == "approv_rider":
                        user_ws[guy_cook] = websocket
                        #rider_data_got = matchUser(guy_cook)
                        #xrider_id = rider_data_got["rider_id"]
                        
                        #if  xrider_id in rider_ws.keys():        
                        #    rider_ws[xrider_id].send(json.dumps(rider_data_got))

                    else:
                        print("no more commands")
        else:
            print("error invalid data")

        print(f"websocket data: {data}")
        #await websocket.send_text(f"Message text was: {data}")

async def logCoords(uuid=str(),user_type=str(),user_coords=dict()):
    response = None
    log_cursor = conn.cursor()
    lat = user_coords["latitude"]
    lon = user_coords["longitude"]
    if user_type == 'customer':
            sql_txt = f"UPDATE `users` SET User_Lon='{lon}',User_Lat='{lat}' WHERE UUID = '{uuid}'"

            log_cursor.execute(sql_txt)
            conn.commit()
            content = {"message": "user coords updated"}
            near_pipo = findRider(uuid,user_coords)
            if near_pipo!=None:
                if len(near_pipo) >0:
                    print(f"near pipo: {near_pipo}")
                    response = JSONResponse(content=near_pipo)
                    nearest_rider = near_pipo[0]
                    guy_cook = nearest_rider['id']
                    
                    print(f"this is a customer {lon}, {lat}")
                    print(f"matched to rider: {guy_cook}")
                    #rider_data_got = matchRider(guy_cook)
                    xrider_id = guy_cook
                    #rider_data_got["rider_id"]
                    print(f"sending to rider: {nearest_rider}")
                    if  xrider_id in rider_ws.keys():
                            usr_data = getUserData(uuid)
                            usr_dic = {}
                            usr_dic["names"] = usr_data[0]
                            usr_dic["tel"] = usr_data[1]
                            usr_dic["coords"] = user_coords

                            ws_dic = {}
                            ws_dic["status"] = 200
                            ws_dic["message"] = usr_dic

                            print(f"using user: {ws_dic}")
                            json_str = json.dumps(ws_dic)
                            print(f"using user string: {json_str}")
                            await rider_ws[xrider_id].send_text(json_str)
                            addOrder(uuid,nearest_rider['id'],user_coords)
                            content = {"status":200,"message": nearest_rider}
                            response = JSONResponse(content=content)
                            
                else:
                    content = {"status":400,"message": "no riders"}
                    response = JSONResponse(content=content)
            else:
                content = {"status":400,"message": "no rider nearby"}
                print("no rider waiting")
                response = JSONResponse(content=content)
            

            response = JSONResponse(content=content)

    elif user_type == 'rider':
            sql_txt = f"UPDATE `riders` SET Rider_Status='1',Rider_Lon='{lon}',Rider_Lat='{lat}' WHERE UUID = '{uuid}'"
            log_cursor.execute(sql_txt)
            conn.commit()
            content = {"status":200,"message": "rider akimbo"}
            response = JSONResponse(content=content)
            print(f"this is a rider {lon}, {lat}")
    else:
            print("user_error")
            content = {"status":404,"message": "user error"}
            response = JSONResponse(content=content)
    log_cursor.close()
    return response

#conn = mysql.connector.connect(**config)

class Customer:
    
    ctable_name = "users"
   
    def __init__(self,name=str(),telephone=str(),passcode=None,user_type=None,uuid=str(),dev_id=str(),fb_id=str()):
        auser_type = "fxuser_customer_type"
        self.msg = str()
        self.bmsg = False
        print(f"adding user {uuid}")
        a_cursor = conn.cursor()
        sql_txt = f"SELECT * FROM `app_users` WHERE CONTACT ='{telephone}' AND PASSCODE = '{passcode}'"

        print(f"execting data {sql_txt}")
        a_cursor.execute(sql_txt)
        data = a_cursor.fetchall()
        print(data)

        if len(data) <= 0:
            sql_in_txt = f"INSERT INTO `app_users`(`NAMES`,`TOKEN`, `CONTACT`,`USER_TYPE`, `PASSCODE`,`DEVICE_ID`,`FB_ID`) VALUES ('{name}','{uuid}','{telephone}','{auser_type}','{passcode}','{dev_id}','{fb_id}')"
            a_cursor.execute(sql_in_txt)
            conn.commit()
            self.msg = "user_added"
            self.bmsg = True
            print("no user")
        else:
            self.msg = "user_active_already"
            print("user already present")
        a_cursor.close()
    def getStatus(self):
        print(f"msg is: {self.msg}")
        return self.msg

class CustomerX:
    
    ctable_name = "users"
   
    def __init__(self,name=str(),telephone=str(),passcode=None,user_type=None,uuid=str(),dev_id=str()):
        self.msg = str()
        self.bmsg = False
        print(f"adding user {uuid}")
        a_cursor = conn.cursor()
        sql_txt = f"SELECT * FROM `users` WHERE User_Contact ='{telephone}' AND passcode = '{passcode}'"

        print(f"execting data {sql_txt}")
        a_cursor.execute(sql_txt)
        data = a_cursor.fetchall()
        print(data)

        if len(data) <= 0:
            sql_in_txt = f"INSERT INTO `users`(`Names`,`UUID`, `User_Contact`, `passcode`) VALUES ('{name}','{uuid}','{telephone}','{passcode}')"
            a_cursor.execute(sql_in_txt)
            conn.commit()
            self.msg = "user_added"
            self.bmsg = True
            print("no user")
        else:
            self.msg = "user_active_already"
            print("user already present")
        a_cursor.close()
    def getStatus(self):
        print(f"msg is: {self.msg}")
        return self.msg

class Rider:
    #conn = mysql.connector.connect(**config)
    #ctable_name = "riders"
    
    def __init__(self,name=str(),telephone=str(),passcode=None,user_type=None,uuid=str(),dev_id=str(),fd_id=str()):
        auser_type = "fxuser_rider_type"
        self.msg = str()
        self.bmsg = False
        print(f"adding user {uuid}")
        a_cursor = conn.cursor()
        sql_txt = f"SELECT * FROM `app_users` WHERE CONTACT ='{telephone}' AND PASSCODE = '{passcode}'"

        print(f"exectinf data {sql_txt}")
        a_cursor.execute(sql_txt)
        data = a_cursor.fetchall()
        print(data)
        #UPDATE `riders` SET `Rider_Status`='0' WHERE 'Rider_Name' = 'maxy';
        if len(data) <= 0:
            rsttatus = False
            sql_in_txt = f"INSERT INTO `app_users`(`TOKEN`,`NAMES`, `CONTACT`,`USER_TYPE`, `PASSCODE`,`DEVICE_ID`,`FB_ID`) VALUES ('{uuid}','{name}','{telephone}','{auser_type}','{passcode}','{dev_id}','{fb_id}')"
            a_cursor.execute(sql_in_txt)
            conn.commit()
            self.bmsg = True
            self.msg = "user_added"
            print("no user")
        else:
            self.msg = "user_active_already"
            print("user already present")
        a_cursor.close()
    def getStatus(self):
        print(f"msg is: {self.msg}")
        return self.msg

class Riderx:
    #conn = mysql.connector.connect(**config)
    #ctable_name = "riders"
    
    def __init__(self,name=str(),telephone=str(),passcode=None,user_type=None,uuid=str()):
        self.msg = str()
        self.bmsg = False
        print(f"adding user {uuid}")
        a_cursor = conn.cursor()
        sql_txt = f"SELECT * FROM `riders` WHERE Rider_Contact ='{telephone}' AND passcode = '{passcode}'"

        print(f"exectinf data {sql_txt}")
        a_cursor.execute(sql_txt)
        data = a_cursor.fetchall()
        print(data)
        #UPDATE `riders` SET `Rider_Status`='0' WHERE 'Rider_Name' = 'maxy';
        if len(data) <= 0:
            rsttatus = False
            sql_in_txt = f"INSERT INTO `riders`(`UUID`,`Rider_Name`, `Rider_Contact`, `passcode`) VALUES ('{uuid}','{name}','{telephone}','{passcode}')"
            a_cursor.execute(sql_in_txt)
            conn.commit()
            self.bmsg = True
            self.msg = "user_added"
            print("no user")
        else:
            self.msg = "user_active_already"
            print("user already present")
        a_cursor.close()
    def getStatus(self):
        print(f"msg is: {self.msg}")
        return self.msg



async def parseReq(request: Request):
    try:
        content = await request.body()
        # Assuming the content is in a form that can be converted to a dictionary, for example, URL-encoded data like "key1=value1&key2=value2"
        data_str = content.decode('utf-8')  # Decode the bytes to a string
        data_list = data_str.split('&')  # Split by "&" to get key-value pairs
        data_dict = {}
        for item in data_list:
            key, value = item.split('=')
            data_dict[key] = value
        return data_dict
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": "Invalid data format"})


def serveUser(request: Request):
    cooky = request.cookies.get("guy_cook")

@app.get("/", response_class=JSONResponse)
async def servePage(request: Request):
    cooky = request.cookies.get("guy_type")
    if cooky == None:
        message = {"status":201}
        return JSONResponse(content=message)
        #return page.TemplateResponse("index.html",{"request": request})
    else:
        cooky_val = "fxpro"+(request.cookies.get("guy_cook"))
        print(f"cookie yeah {cooky_val}")
        if cooky == "customer":
            user_data = getUserData(cooky_val)
            message = {"status":200,"body":{"user_names":user_data[0],"user_type":"customer"}}
            return JSONResponse(content=message)
            #return page.TemplateResponse("user.html",{"request": request,'fast_user_names':user_data[0],'fast_user_type':'customer'})
        elif cooky == "rider":

            rider_data = getRiderData(cooky_val)
            message = {"status":200,"body":{"user_names":rider_data[0],"user_type":"rider"}}
            return JSONResponse(content=message)
            #return page.TemplateResponse("rider.html",{"request": request,'fast_user_names':rider_data[0],'fast_user_type':'rider'})
        else:
            message = {"status":400}
            return JSONResponse(content=message)
            #return None

@app.get("/red", response_class=HTMLResponse)
async def reservePage(request: Request):
    cooky = request.cookies.get("guy_cook")
    if cooky == None:
        return page.TemplateResponse("user.html",{"request": request})
    else:
        await register_user(request)

@app.post("/registerx")
async def regUser(request: Request):
    req_data = await request.json()
    print(req_data)#["name"])
    redirect_url = "/red"
    print(f"url is: {redirect_url}\n\n")
    content = {"status":200,"redirect":redirect_url}
    response_json = JSONResponse(content)
    return response_json
    #RedirectResponse(redirect_url,status_code=status.HTTP_302_FOUND)

@app.post("/orderRide")
async def completeOrder(request:Request):
    req_data = await request.json()
    print(req_data)

#byadala by alienskin
def findDetailsByDevId(dev_idx=str()):
    usql = f"SELECT NAMES,CONTACT FROM app_users WHERE DEVICE_ID = '{dev_idx}'"
    driver_checks = conn.cursor()
    driver_checks.execute(usql)
    drivers = driver_checks.fetchall()
    return drivers

def findDetailsByToken(token_id=str()):
    usql = f"SELECT NAMES,CONTACT,USER_TYPE,DEVICE_ID,FB_ID FROM app_users WHERE TOKEN = '{token_id}'"
    driver_checks = conn.cursor()
    driver_checks.execute(usql)
    drivers = driver_checks.fetchall()[0]
    return drivers


def findOrderByID(order_id=str()):
    usql = f"SELECT DEV_ID,DRIVER_ID,ORDER_HANDLE,ORDER_DATA FROM hyperorders WHERE ORDER_ID = '{order_id}'"
    driver_checks = conn.cursor()
    driver_checks.execute(usql)
    drivers = driver_checks.fetchall()[0]
    return drivers

def initDriver(udev_id=str(),order_id=str()):

    isql_txt = f"SELECT DRIVER_ID,ORDER_DATA FROM hyperorders WHERE ORDER_ID = '{order_id}' AND DEV_ID = '{udev_id}'"
    init_ctrl = conn.cursor()
    init_ctrl.execute(isql_txt)

    drivers = init_ctrl.fetchall()
    print(f"found drivers {drivers}")
    if len(drivers)>0:
        driva_id = drivers[0][0]
        order_datum = drivers[0][1]
        print(f"found id {driva_id} and order {order_datum}")
        final_sql = f"SELECT FB_ID FROM app_users WHERE DEVICE_ID = '{driva_id}'"
        init_ctrl.execute(final_sql)

        fb_ids = init_ctrl.fetchall()
        print(f"found ids {fb_ids}")

        if(len(fb_ids)>0):
            fb_id=fb_ids[0][0]
            jorder_datum = json.loads(order_datum)
            customer_dta = findDetailsByDevId(udev_id)
            or_data={
                "order_id": order_id,
                "order_details":{
                "customer_name":customer_dta[0][0],
                "customer_contact":customer_dta[0][1],
                "customer_coords": jorder_datum["order_src"],
                "order_dest":jorder_datum["order_dest"]
                                }  # Your JSON data here
                 }
            fb_mod.ping(fb_id,or_data,"order_200")
            print("\ndriver init")



def addDriver(devID,drivaID,orderHandle,order_data):
    #order_id = str(uuid.uuid4())
    jorder_data = json.dumps(order_data)
    #usql = f"INSERT INTO hyperorders(ORDER_ID,DEV_ID,DRIVER_ID,ORDER_HANDLE,ORDER_DATA) VALUES (UUID(),'{devID}','{drivaID}','{orderHandle}','{jorder_data}')"
    usql = f"UPDATE hyperorders SET ORDER_HANDLE='{orderHandle}' WHERE DEV_ID='{devID}' AND DRIVER_ID='{drivaID}'"
    a_cursor = conn.cursor()
    a_cursor.execute(usql)
    conn.commit()

def raw_addDriver(devID,drivaID,order_data):
    order_id = str(uuid.uuid4())
    jorder_data = json.dumps(order_data)
    usql = f"INSERT INTO hyperorders(ORDER_ID,DEV_ID,DRIVER_ID,ORDER_DATA) VALUES ('{order_id}','{devID}','{drivaID}','{jorder_data}')"
    a_cursor = conn.cursor()
    a_cursor.execute(usql)
    conn.commit()
    return order_id

def authUser(user_tel=str(),user_pwd=str(),dev_id=str(),fb_id=str()):

    usql_txt = f"SELECT TOKEN,DEVICE_ID,USER_TYPE,NAMES,FB_ID FROM app_users WHERE CONTACT = '{user_tel}' AND PASSCODE = '{user_pwd}'"
    #rsql_txt = f"SELECT TOKEN FROM app_users WHERE CONTACT = '{user_tel}'"

    update_devID = f"UPDATE app_users SET DEVICE_ID = '{dev_id}' WHERE CONTACT = '{user_tel}' AND PASSCODE = '{user_pwd}'"
    update_fbID = f"UPDATE app_users SET FB_ID = '{fb_id}' WHERE CONTACT = '{user_tel}' AND PASSCODE = '{user_pwd}'"
    user_chcks = conn.cursor()
    user_chcks.execute(usql_txt)

    uuids = user_chcks.fetchall()
    print(f"uuids: {uuids}")
    res_uuid = list()
    if len(uuids) > 0:
        usr_uuid = uuids[0][0]
        usr_id = uuids[0][1]
        usr_type = uuids[0][2]
        usr_name = uuids[0][3]
        usr_fb_id = uuids[0][4]

        if(usr_type == "fxuser_customer_type"):
            print(f"gotten user uuid {usr_uuid}")
        #res_uuid = {}
        #res_uuid = usr_uuid

            res_uuid.append("customer")
            res_uuid.append(usr_uuid)
            res_uuid.append(usr_name)

            if(dev_id != usr_id):
                print("device id changed")
                user_chcks.execute(update_devID)
                conn.commit()

                hyper_mod.del_device(usr_id)
                update_stat = 204
                hyper_mod.set_dev_name(dev_id,"winston_user_"+user_tel)
                if update_stat == 204:
                    print("Update successful")
                else:
                    print(f"update error: {update_stat}")
    
            if(fb_id != usr_fb_id):
                print("device id changed")
                user_chcks.execute(update_fbID)
                conn.commit()

                #hyper_mod.del_device(usr_id)
                #update_stat = 204
                #hyper_mod.set_dev_name(dev_id,"winston_user_"+user_tel)
                #if update_stat == 204:
                print("firebase Update successful")
                #else:
                #    print(f"update error: {update_stat}")


        elif(usr_type == "fxuser_rider_type"):
            print(f"gotten rider uuid {usr_uuid}")
            res_uuid.append("rider")
            res_uuid.append(usr_uuid)
            res_uuid.append(usr_name)
            #res_uuid = ruuid
            if(dev_id != usr_id):
                print("device id changed")
                user_chcks.execute(update_devID)
                conn.commit()

                update_stat = hyper_mod.update_driver(user_tel,dev_id)
                if update_stat == 200:
                    print("Update successful")
                else:
                    print(f"update error: {update_stat}")
            
            if(fb_id != usr_fb_id):
                print("device id changed")
                user_chcks.execute(update_fbID)
                conn.commit()

                #hyper_mod.del_device(usr_id)
                #update_stat = 204
                #hyper_mod.set_dev_name(dev_id,"winston_user_"+user_tel)
                #if update_stat == 204:
                print("firebase Update successful")
    print(f"sending uuids {res_uuid}")
    return res_uuid

def authUserx(user_tel=str(),user_pwd=str()):

    usql_txt = f"SELECT UUID FROM users WHERE User_Contact = '{user_tel}'"
    rsql_txt = f"SELECT UUID FROM riders WHERE Rider_Contact = '{user_tel}'"

    user_chcks = conn.cursor()
    user_chcks.execute(usql_txt)

    uuids = user_chcks.fetchall()
    print(f"uuids: {uuids}")
    res_uuid = list()
    if len(uuids) > 0:
        usr_uuid = uuids[0][0]
        print(f"gotten user uuid {usr_uuid}")
        #res_uuid = {}
        #res_uuid = usr_uuid

        res_uuid.append("customer")
        res_uuid.append(usr_uuid)
    else:
        user_chcks.execute(rsql_txt)
        ruuids = user_chcks.fetchall()

        if len(ruuids) > 0:
            ruuid = ruuids[0][0]
            print(f"gotten rider uuid {ruuid}")
            res_uuid.append("rider")
            res_uuid.append(ruuid)
            #res_uuid = ruuid
    print(f"sending uuids {res_uuid}")
    return res_uuid


@app.post("/login")
async def login_user(request: Request):
    
    json_request = await request.json()
    print(json_request)
    user_tel = json_request["telephone"]
    user_pwd = json_request["passcode"]
    dev_id = json_request["dev_id"]
    fb_id = json_request["fb_id"]
    map_url = hyper_mod.gen_device_map(dev_id)
    cook = authUser(user_tel,user_pwd,dev_id,fb_id)
    response = None
    print(f"cooking {cook}")
    if len(cook) > 0:
        print(cook)
        redirect_url = cook[0]#"/"
        print(f"redirect url is : {redirect_url}")
        jcontent = {"status":200,"redirect":redirect_url,"app_man":cook[2],"map_man":map_url}
        response = JSONResponse(content = jcontent)
        response.set_cookie(key="guy_type",value=cook[0].replace("fxpro",''))
        response.set_cookie(key="guy_cook",value=cook[1].replace("fxpro",''))
    else:
         jcontent = {"status":404,"message":"user error"}
         response = JSONResponse(content = jcontent)
    return response





@app.post("/register")
async def register_user(request: Request):
    cooky = request.cookies.get("guy_cook")
    print(f"cookie: {cooky}")
    redirect_url = "customer"
    customer = None
    response = None
    if cooky == None:
        print("NO COOKIE")
        
    else:
        print("COOKIE HERE")
        #content = {"message": "cookie login succes"}
        #response = JSONResponse(content=content)
        #return response
        #customer = cooky_dic[cooky]
    #return response
    customer = await request.json()
    name = customer['name']
        
    telno = customer['telephone']
    cpass = customer['passcode']
    user_type = customer['user_type']
    cdev_id = customer['dev_id']

    if user_type == "customer":
        redirect_url = "customer"
        new_uuid = str(uuid.uuid4())
        print(f"uuid is: {new_uuid}")
        customer["uuid"] = "fxpro"+new_uuid
        cuuid = customer["uuid"]
        print(f"uuid is: {cuuid}")
        print(f"customer is {customer}")
        user_o = Customer(**customer)
        if user_o.getStatus() == "user_added":
            content = {"status":200,"redirect":redirect_url}
            response = JSONResponse(content=content)
            response.set_cookie(key="guy_cook", value=new_uuid)
            response.set_cookie(key="guy_type",value = user_type)

            hyper_res = hyper_mod.set_dev_name(cdev_id,"winston_user_"+telno)
            #if hyper_res.status_code == 204:
            print("user hyper track created")
            #else:
            #    print("\nfailed to create hypertrack user")
        #cooky_dic[cuuid] = customer
            print(f"user at: {customer['name']}")
        elif user_o.getStatus() == "user_active_already":
            content = {"status":200,"redirect":redirect_url}
            #response = JSONResponse(content=content)
        else:
            content = {"message": "login error"}
            response = JSONResponse(content=content)
    elif user_type == "rider":
        redirect_url = "rider"
        rnew_uuid = str(uuid.uuid4())
        print(f"uuid is: {rnew_uuid}")
        customer["uuid"] = "fxpro"+rnew_uuid
        rcuuid = customer["uuid"]
        print(f"uuid is: {rcuuid}")
        print(f"rider is {customer}")
        rider_o = Rider(**customer)
        rstat = rider_o.getStatus() 
        if rstat == "user_added":
            print('user added')
            mkstatus = hyper_mod.create_driver(telno,cdev_id,name)

            if mkstatus == 201:
                rcontent = {"message": "login succes"}
                content = {"status":200,"redirect":redirect_url}
                response = JSONResponse(content=content)
            else:
                content = {"status":404,"message":"driver failed"}
                response = JSONResponse(content=content)
            response.set_cookie(key="guy_cook", value=rnew_uuid)
            response.set_cookie(key="guy_type",value = user_type)
        elif rider_o.getStatus() == "user_active_already":
            content = {"message": "cookie ll login succes"}
            content = {"status":200,"redirect":redirect_url}
            response = JSONResponse(content=content)
        else:
            content = {"message": "login error"}
            response = JSONResponse(content=content)
        #cooky_dic[rcuuid] = customer
        print(f"rider at: {customer['name']}")
        
    else:
        content = {"message": "invalid user"}
        response = JSONResponse(content=content)
    redirect_url = "/red"
    print(f"url is: {redirect_url}\n\n")
    
    #response_json = JSONResponse(content)
    return response
    #return response

@app.post("/lookrider")
async def riderEye(request: Request):
    print(cooky_dic)
    cooky = request.cookies.get("guy_cook")
    cook_type = request.cookies.get("guy_type")
    print(f"cookie: {cooky}")
    print(f"cookie_type: {cook_type}")
    customer = None
    response = None
    if cooky == None:
        print("NO COOKIE")
        content = {"status":401,"message": "please login 1st"}
        response = JSONResponse(content=content)
        return response
    else:
        print("COOKIE HERE")
        active_point = "fxpro"+cooky
        #cooky_dic["fxpro"+cooky]
        active_coords = await request.json()
        alat = active_coords["latitude"]
        alon = active_coords["longitude"]
        print(f"coords are: {alat} and {alon}")
        auser_type = cook_type

        if auser_type == 'customer':
            print("this is a customer")
            to_alat = active_coords["to_latitude"]
            to_alon = active_coords["to_longitude"]
            udev_id = active_coords["dev_id"]
            drivers = []
            #response = await logCoords(active_point,auser_type,active_coords)
            near_byo = hyper_mod.get_nearby_rider(alon,alat)
            #near_byo = hyper_mod.get_nearby(alon,alat)
            #near_bys = hyper_mod.get_nearby(alon,alat)
            
            near_byo_status_code = 200
            if (near_byo_status_code == 200):
                near_bys = near_byo#.json()
                print(near_bys)
                print("driver oned")
                for near_bya in near_bys["drivers"]:
                    rider_id = near_bya['device']['device_id']
                    #usr_details = findDetailsByDevId(near_bya['device']['device_id'])
                    usr_details = findDetailsByDevId(rider_id)
                    if len(usr_details) >0:
                        geom = near_bya["location"]["geometry"]
                        
                        #addDriver(udev_id,rider_id)
                        order_dta = {"order_src":[alat,alon],"order_dest":[to_alat,to_alon]}
                        or_id = raw_addDriver(udev_id,rider_id,order_dta)
                        usr_json = {"status":200,"order_id":or_id,"name":usr_details[0][0],"contact":usr_details[0][1],"geo_data":geom}
                        driver_json = {"details":usr_json}
                        drivers.append(driver_json)

                        #oresponse = hyper_mod.gen_walk_order(rider_id,alon,alat)
                        #print(f"order daata: {oresponse.json()}")
                        #print(f"order status: {oresponse.status_code}")
                        #if oresponse.status_code == 201:
                        #    oresponse_json =  oresponse.json()
                        #    print(f"order {oresponse_json}")
                        #    order_content = {"track_point": oresponse_json["orders"][0]["share_url"],"handle":oresponse_json["orders"][0]["order_handle"]}
                            
                        #    driver_json = {"details":usr_json,"order_data":order_content}
                        #    addDriver(cooky,rider_id,oresponse_json["orders"][0]["order_handle"],driver_json)
                        #    drivers.append(driver_json)
                        #    #drivers.append(usr_json)
                        #    print("order created well")
                            #response = JSONResponse(content=content)
                        #else:
                        #    print("error creating order")
                    else:
                        print("no driver found")
                   
            else:
                print("driver not oned")
            print("this is a rider")
            if len(drivers)>0:
                content = {"status":200,"message": drivers}
                response = JSONResponse(content=content)
            else:
                content = {"status":400,"message": "no drivers found"}
                response = JSONResponse(content=content)
            return response
            
        elif auser_type == 'rider':
            to_alat = active_coords["to_latitude"]
            to_alon = active_coords["to_longitude"]
            rider_details=findDetailsByToken(active_point)
            driva_handle = f"fx_winston_driver_{rider_details[1]}"
            print("driver handle is ",driva_handle)
            #response = await logCoords(active_point,auser_type,active_coords)
            stat_data = hyper_mod.set_driver_status(driva_handle,True)
            print(stat_data.json())
            if (stat_data.status_code == 200):
                print("driver oned")
            else:
                print("driver not oned")
            print("this is a rider")
            content = {"status":200,"message": "driver activated"}
            response = JSONResponse(content=content)
            return response
        else:
            print("user_error")
            content = {"message": "user error"}
            response = JSONResponse(content=content)
        return response
    print("lookup driver")

@app.post("/orders")
async def riderEye(request: Request):
    print(cooky_dic)
    cooky = request.cookies.get("guy_cook")
    cook_type = request.cookies.get("guy_type")
    print(f"cookie: {cooky}")
    print(f"cookie_type: {cook_type}")
    customer = None
    response = None
    if cooky == None:
        print("NO COOKIE")
        content = {"status":401,"message": "please login 1st"}
        response = JSONResponse(content=content)
        return response
    else:
        print("COOKIE HERE")
        active_point = "fxpro"+cooky
        #cooky_dic["fxpro"+cooky]
        active_coords = await request.json()
        
        auser_type = cook_type

        if auser_type == 'customer':
            print("this is a customer")
            drivers = []
            #response = await logCoords(active_point,auser_type,active_coords)
            near_byo = hyper_mod.get_nearby(alon,alat)
            near_bys = near_byo.json()
            #near_bys = hyper_mod.get_nearby(alon,alat)
            print(near_bys)
            #near_byo_status_code = 200
            if (near_byo.status_code == 200):
                print("driver oned")
                for near_bya in near_bys["drivers"]:
                    rider_id = near_bya['device']['device_id']
                    #usr_details = findDetailsByDevId(near_bya['device']['device_id'])
                    usr_details = findDetailsByDevId(rider_id)
                    if len(usr_details) >0:
                        geom = near_bya["location"]["geometry"]
                        usr_json = {"status":200,"name":usr_details[0][0],"contact":usr_details[0][1],"geo_data":geom}
                        
                        oresponse = hyper_mod.gen_walk_order(rider_id,alon,alat)
                        print(f"order daata: {oresponse.json()}")
                        print(f"order status: {oresponse.status_code}")
                        if oresponse.status_code == 201:
                            oresponse_json =  oresponse.json()
                            print(f"order {oresponse_json}")
                            order_content = {"track_point": oresponse_json["orders"][0]["share_url"],"handle":oresponse_json["orders"][0]["order_handle"]}
                            
                            driver_json = {"details":usr_json,"order_data":order_content}
                            addDriver(cooky,rider_id,oresponse_json["orders"][0]["order_handle"],driver_json)
                            drivers.append(driver_json)
                            #drivers.append(usr_json)
                            print("order created well")
                            #response = JSONResponse(content=content)
                        else:
                            print("error creating order")
                    else:
                        print("no driver found")
                   
            else:
                print("driver not oned")
            print("this is a rider")
            if len(drivers)>0:
                content = {"status":200,"message": drivers}
                response = JSONResponse(content=content)
            else:
                content = {"status":400,"message": "no drivers found"}
                response = JSONResponse(content=content)
            return response
            
        elif auser_type == 'rider':
            #to_alat = active_coords["to_latitude"]
            #to_alon = active_coords["to_longitude"]
            #driva_handle = f"fx_winston_driver_{active_point}"
            ##response = await logCoords(active_point,auser_type,active_coords)
            #stat_data = hyper_mod.set_driver_status(driva_handle,True)
            #print(stat_data.json())
            #if (stat_data.status_code == 200):
            #    print("driver oned")
            #else:
            #    print("driver not oned")
            #print("this is a rider")
            
            order_data = riderOrderCtrl(**active_coords)
            if (len(order_data)>0):
                content = {"status":200,"message": order_data}
                response = JSONResponse(content=content)
            else:
                content = {"status":400,"message": order_data}
                response = JSONResponse(content=content)
            return response
        else:
            print("user_error")
            content = {"message": "user error"}
            response = JSONResponse(content=content)
        return response
    print("lookup driver")

@app.post("/cancel_scan")
async def riderEye(request: Request):
    print(cooky_dic)
    cooky = request.cookies.get("guy_cook")
    cook_type = request.cookies.get("guy_type")
    print(f"cookie: {cooky}")
    print(f"cookie_type: {cook_type}")
    customer = None
    response = None
    if cooky == None:
        print("NO COOKIE")
        content = {"status":401,"message": "please login 1st"}
        response = JSONResponse(content=content)
        return response
    else:
        print("COOKIE HERE")
        active_point = "fxpro"+cooky
        #cooky_dic["fxpro"+cooky]
        active_coords = await request.json()
        alat = active_coords["latitude"]
        alon = active_coords["longitude"]
        print(f"coords are: {alat} and {alon}")
        auser_type = cook_type

        if auser_type == 'customer':
            print("this is a customer")
            #response = await logCoords(active_point,auser_type,active_coords)
            
        elif auser_type == 'rider':
            to_alat = active_coords["to_latitude"]
            to_alon = active_coords["to_longitude"]
            driva_handle = f"fx_winston_driver_{active_point}"
            #response = await logCoords(active_point,auser_type,active_coords)
            stat_data = hyper_mod.set_driver_status(driva_handle,False)
            print(stat_data.json())
            if (stat_data.status_code == 200):
                print("driver oned")
            else:
                print("driver not oned")
            print("this is a rider")
            content = {"status":200,"message": "driver deactivated"}
            response = JSONResponse(content=content)
            return response
        else:
            print("user_error")
            content = {"message": "user error"}
            response = JSONResponse(content=content)
        return response
    print("lookup driver")

@app.post("/lookwalker")
async def riderEye(request: Request):
    print(cooky_dic)
    cooky = request.cookies.get("guy_cook")
    cook_type = request.cookies.get("guy_type")
    print(f"cookie: {cooky}")
    print(f"cookie_type: {cook_type}")
    customer = None
    response = None
    if cooky == None:
        print("NO COOKIE")
        content = {"status":401,"message": "please login 1st"}
        response = JSONResponse(content=content)
        return response
    else:
        print("COOKIE HERE")
        active_point = "fxpro"+cooky
        #cooky_dic["fxpro"+cooky]
        active_coords = await request.json()
        alat = active_coords["to_latitude"]
        alon = active_coords["to_longitude"]
        atel = active_coords["user_tel"]
        adev_id = active_coords["dev_id"]
        print(f"coords are: {alat} and {alon}")
        auser_type = cook_type

        if auser_type == 'customer':
            print("this is a customer")
            oresponse = hyper_mod.gen_walk_order(adev_id,alon,alat)
            print(f"order status: {oresponse.status_code}")
            if oresponse.status_code == 201:
                oresponse_json =  oresponse.json()
                content = {"status":200,"order":{"track_point": oresponse_json["orders"][0]["share_url"],"handle":oresponse_json["orders"][0]["order_handle"]}}
                print("order created well")
                response = JSONResponse(content=content)
            else:
                print("error creating order")
            #await logCoords(active_point,auser_type,active_coords)
            
        elif auser_type == 'rider':
            #response = await logCoords(active_point,auser_type,active_coords)
            print("this is a rider")
        else:
            print("user_error")
            content = {"message": "user error"}
            response = JSONResponse(content=content)
        return response


@app.post("/approv_rider")
async def riderEye(request: Request):
    print(cooky_dic)
    cooky = request.cookies.get("guy_cook")
    cook_type = request.cookies.get("guy_type")
    print(f"cookie: {cooky}")
    print(f"cookie_type: {cook_type}")
    customer = None
    response = None
    if cooky == None:
        print("NO COOKIE")
        content = {"status":401,"message": "please login 1st"}
        response = JSONResponse(content=content)
        return response
    else:
        print("COOKIE HERE")
        active_point = "fxpro"+cooky
        #cooky_dic["fxpro"+cooky]
        active_coords = await request.json()
        rider_cursor = active_coords["cursor"]
        #alat = active_coords["to_latitude"]
        #alon = active_coords["to_longitude"]
        #atel = active_coords["user_tel"]
        #adev_id = active_coords["dev_id"]
        #print(f"coords are: {alat} and {alon}")
        auser_type = cook_type

        if auser_type == 'customer':
            active_order = active_coords["order_id"]
            active_device = active_coords["dev_id"]
            print(f"in data {active_coords}")

            print("this is a customer")
            #oresponse = hyper_mod.gen_walk_order(adev_id,alon,alat)
          #  print(f"order status: {oresponse.status_code}")
            #if oresponse.status_code == 201:
            #    oresponse_json =  oresponse.json()
            #    content = {"status":200,"order":{"track_point": oresponse_json["orders"][0]["share_url"],"handle":oresponse_json["orders"][0]["order_handle"]}}
            #    print("order created well")
            #    response = JSONResponse(content=content)
            ##else:
            #    print("error creating order")
            #await logCoords(active_point,auser_type,active_coords)
            initDriver(active_coords["dev_id"],active_coords["order_id"])
            print("driver init okay")
            content = {"status":200}#"order":{"track_point": oresponse_json["orders"][0]["share_url"],"handle":oresponse_json["orders"][0]["order_handle"]}}
            response = JSONResponse(content=content)
            print("order created well")
            
        elif auser_type == 'rider':
            #response = await logCoords(active_point,auser_type,active_coords)
            print("this is a rider")
        else:
            print("user_error")
            content = {"message": "user error"}
            response = JSONResponse(content=content)
        return response

@app.post("/cancelOrder")
async def riderEye(request: Request):
    print(cooky_dic)
    cooky = request.cookies.get("guy_cook")
    cook_type = request.cookies.get("guy_type")
    print(f"cookie: {cooky}")
    print(f"cookie_type: {cook_type}")
    customer = None
    response = None
    if cooky == None:
        print("NO COOKIE")
        content = {"status":401,"message": "please login 1st"}
        response = JSONResponse(content=content)
        return response
    else:
        print("COOKIE HERE")
        active_point = "fxpro"+cooky
        #cooky_dic["fxpro"+cooky]
        active_coords = await request.json()
        #alat = active_coords["to_latitude"]
        #alon = active_coords["to_longitude"]
        #atel = active_coords["user_tel"]
        adev_id = active_coords["dev_id"]
        #adev_handle = active_coords["dev_handle"]
        aord_id = active_coords["order_id"]
        #print(f"order handle is {adev_handle}")
        auser_type = cook_type

        if auser_type == 'customer':
            print("this is a customer")
            findDetailsByToken(active_point)
            delRide(adev_id)
            #oresponse = hyper_mod.cancel_order(adev_handle)
            #print(f"order status: {oresponse.status_code}")
            #if oresponse.status_code == 200:
            #    oresponse_json =  oresponse.json()
            #    print(f"order cancel {oresponse_json}")
            #    content = {"status":200}
                #:{"track_point": oresponse_json["orders"][0]["share_url"],"handle":oresponse_json["orders"][0]["order_handle"]}}
            #    print("order created well")
            #    response = JSONResponse(content=content)
            #else:
            #    print("error creating order")
            #await logCoords(active_point,auser_type,active_coords)
            content = {"status":200}
                #:{"track_point": oresponse_json["orders"][0]["share_url"],"handle":oresponse_json["orders"][0]["order_handle"]}}
            #    print("order created well")
            response = JSONResponse(content=content)
        elif auser_type == 'rider':
            
            riderdata = findDetailsByToken(active_point)
            rider_dev = riderdata[3]

            if(rider_dev  == adev_id):
                print("finding order: ",aord_id)
                order_dt = findOrderByID(aord_id)
                
                order_handle = order_dt[2]
                # "winston_ride_order_fx_winston_driver_702891117"
                #order_dt[2]
                print("deleting order handle ",order_handle)
                delOrder(aord_id,order_handle)

            print("device id is ",rider_dev)
            content = {"status":200}
            response = JSONResponse(content=content)
            #response = await logCoords(active_point,auser_type,active_coords)
            print("this is a rider")
        else:
            print("user_error")
            content = {"message": "user error"}
            response = JSONResponse(content=content)
        return response
    print("lookup driver")


async def riderEyeX(request: Request):
    print(cooky_dic)
    cooky = request.cookies.get("guy_cook")
    cook_type = request.cookies.get("guy_type")
    print(f"cookie: {cooky}")
    print(f"cookie_type: {cook_type}")
    customer = None
    response = None
    if cooky == None:
        print("NO COOKIE")
        content = {"status":401,"message": "please login 1st"}
        response = JSONResponse(content=content)
        return response
    else:
        print("COOKIE HERE")
        active_point = "fxpro"+cooky
        #cooky_dic["fxpro"+cooky]
        active_coords = await request.json()
        alat = active_coords["latitude"]
        alon = active_coords["longitude"]
        print(f"coords are: {alat} and {alon}")
        auser_type = cook_type

        if auser_type == 'customer':
            print("this is a customer")
            response = await logCoords(active_point,auser_type,active_coords)
        elif auser_type == 'rider':
            response = await logCoords(active_point,auser_type,active_coords)
            print("this is a rider")
        else:
            print("user_error")
            content = {"message": "user error"}
            response = JSONResponse(content=content)
        return response
    print("lookup driver")


@app.post("/drivers/")
def register_driver(name: str, latitude: float, longitude: float):
    driver_id = str(uuid.uuid4())
    driver = Driver(id=driver_id, name=name, latitude=latitude, longitude=longitude)

    db = SessionLocal()
    db.add(driver)
    db.commit()
    db.close()

    return driver

@app.post("/ride-requests/")
def submit_ride_request(user_latitude: float, user_longitude: float, dest_latitude: float, dest_longitude: float):
    request_id = str(uuid.uuid4())
    ride_request = RideRequest(
        id=request_id,
        user_latitude=user_latitude,
        user_longitude=user_longitude,
        dest_latitude=dest_latitude,
        dest_longitude=dest_longitude,
    )

    #db = SessionLocal()
    #db.add(ride_request)
    #db.commit()
    #db.close()

    # Find the nearest available driver and assign the ride request to them
    nearest_driver = find_nearest_driver(ride_request.id, ride_request.user_latitude, ride_request.user_longitude)
    if nearest_driver:
        ride_request.status = "accepted"
        ride_request.assigned_driver_id = nearest_driver.id
    else:
        ride_request.status = "pending"

    #db = SessionLocal()
    #db.add(ride_request)
    #db.commit()
    #db.close()

    return ride_request

#def find_nearest_driver(ride_request_id, user_latitude, user_longitude):
def find_nearest_driver(user_location):
    # Define a maximum distance for considering drivers
    max_distance_km = 10.0

    drivers = []
    for data in driver_data:
        driver = Driver(name=data["name"], latitude=data["latitude"], longitude=data["longitude"])
        drivers.append(driver)

    available_drivers = [driver for driver in drivers if not any(request.assigned_driver.id == driver.id for request in ride_requests)]
    
    if not available_drivers:
        return None

    nearest_driver = min(available_drivers, key=lambda driver: geodesic(driver.location, user_location).kilometers)

    if geodesic(nearest_driver.location, user_location).kilometers > max_distance_km:
        return None

    return nearest_driver

@app.put("/ride-requests/{ride_request_id}/response/")
def driver_response(ride_request_id: str, status: str):
    db = SessionLocal()
    ride_request = db.query(RideRequest).filter(RideRequest.id == ride_request_id).first()

    if not ride_request:
        db.close()
        raise HTTPException(status_code=404, detail="Ride request not found.")

    if ride_request.status == "pending":
        db.close()
        raise HTTPException(status_code=400, detail="Ride request has not been accepted yet.")

    if status.lower() == "accept":
        ride_request.status = "accepted"
    elif status.lower() == "decline":
        ride_request.status = "declined"
    else:
        db.close()
        raise HTTPException(status_code=400, detail="Invalid response status.")

    db.commit()
    db.close()

    return ride_request
