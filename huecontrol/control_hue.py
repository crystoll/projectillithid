#!/usr/bin/python
import time
from phue import Bridge



PARAM_STATE='on'
PARAM_BRIGHTNESS='bri'
PARAM_NAME='name'

bridge_ip_address = '192.168.0.2'
lamp_name='Cornerlight'


def get_light_ids(api):
    lights_info = api['lights']
    lamp_ids = [int(key) for key, value in lights_info.items()]
    return lamp_ids


def get_light_names(api):
    lights_info = api['lights']
    lamp_names = [value['name'] for key, value in lights_info.items()]
    return lamp_names


b = Bridge(bridge_ip_address)

# If the app is not registered and the button is not pressed, press the button and call connect() (this only needs to be run a single time)
# b.connect()

# Get the bridge state (This returns the full dictionary that you can explore)
api = b.get_api()

# Get light names and ids from API if necessary
#light_ids = get_light_ids(api)
#light_names = get_light_names(api)
#print(light_ids)
#print(light_names)

b.set_light(lamp_name, PARAM_STATE, True)
#b.set_light(lamp_name, PARAM_BRIGHTNESS,0) # 0 to 254
command =  {'transitiontime' : 100, 'on' : True, 'bri' : 0}
b.set_light(lamp_name, command)
