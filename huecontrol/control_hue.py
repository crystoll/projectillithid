#!/usr/bin/python
import time
from phue import Bridge



PARAM_TURNEDON='on'
PARAM_BRIGHTNESS='bri'
PARAM_NAME='name'
PARAM_HUE='hue'
PARAM_SATURATION='sat'
PARAM_STATE='state'
PARAM_EFFECT='effect'

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

def increase_intensity(b,lamp_name):
    light = b.get_light(lamp_name)
    bri = light[PARAM_STATE][PARAM_BRIGHTNESS] # 0 to 254
    hue = light[PARAM_STATE][PARAM_HUE] # 0 to 65535
    sat = light[PARAM_STATE][PARAM_SATURATION] # 0 to 254
    if bri < 244:
        bri += 10
        b.set_light(lamp_name, PARAM_BRIGHTNESS,bri)
    else:
        b.set_light(lamp_name, PARAM_BRIGHTNESS,0, transitiontime=0.5)
        b.set_light(lamp_name, PARAM_BRIGHTNESS, 254, transitiontime=0.5)
    if sat < 244:
        sat += 10
        b.set_light(lamp_name, PARAM_SATURATION,sat)

#    if hue < 40000:
#        hue += 100
#        b.set_light(lamp_name, PARAM_HUE, hue)


bridge = Bridge(bridge_ip_address)

# If the app is not registered and the button is not pressed, press the button and call connect() (this only needs to be run a single time)
# b.connect()

# Get the bridge state (This returns the full dictionary that you can explore)
api = bridge.get_api()

# Get light names and ids from API if necessary
#light_ids = get_light_ids(api)
#light_names = get_light_names(api)
#print(light_ids)
#print(light_names)

bridge.set_light(lamp_name, PARAM_TURNEDON, True)
bridge.set_light(lamp_name, PARAM_HUE, 65535)
bridge.set_light(lamp_name, PARAM_SATURATION, 0)
bridge.set_light(lamp_name, PARAM_BRIGHTNESS, 0)
bridge.set_light(lamp_name, PARAM_EFFECT, 'none') # colorloop or none supported


#b.set_light(lamp_name, PARAM_BRIGHTNESS,0) # 0 to 254
#command =  {'transitiontime' : 100, 'on' : True, 'bri' : 0}
#bridge.set_light(lamp_name, command)

while True:
    increase_intensity(bridge, lamp_name)
    time.sleep(1)
