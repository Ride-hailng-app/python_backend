import hypertrack
#import hyper_mod
api_key = "HpnYbs5tz4fhd_oAYQHIxcLvXlk"
sec_key = "11rNJqLL5wDrRyhmbIH2TVQeJiEObLx398EKHoB7aq_e-RMtOGsc6Q"
#dev_id = "001FA236-3678-480E-A6BE-E5DFB54F71EE"
dev_idx	=	"6869749E-5D2A-4B25-A263-3EF17BD03826"
dev_id = "C032CC75-4D47-4EDE-8365-DC3D55A60100"
def locs(updates):
	print(updates)
client = hypertrack.Client(api_key,sec_key)

data = {'name': 'marksman', 'vehicle_type': 'bajaj', 'phone': '+256702891117', 'fleet_id': "941503-8beb-4bf8-9093-831bf070e9d6"}
#driver = hypertrack.Drivers
#.create(**data)

#client.devices.set_available("")
tra = client.devices.start_tracking(dev_id)
#print(tra)
tr = client.devices.get(dev_id)#_history(dev_id,"2023-09-2")
#client.on_location_update(dev_id,locs)
#print(hyper_mod.del_device(dev_id))#"sony_test"))
#print(loc)
print(tr)
