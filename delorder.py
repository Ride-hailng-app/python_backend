import hyper_mod
#del_order = "winston_ride_order_fx_winston_driver_fxpro6cf645d7-fdca-4d83-b335-9b50bbe8d942"
#"winston_walker_order_F149C7BA-EBFB-4B72-B48A-369F55ABD653"
#"winston_walker_order_D6D603A7-6F8C-43AB-886D-5100D4F290B4"
del_order = "winston_ride_order_fx_winston_driver_702891117"
stat = hyper_mod.cancel_order(del_order)

print(stat.status_code)
print(stat.json())