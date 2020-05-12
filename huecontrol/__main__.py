import time

from .mindwave.mindwave import Headset
from .hue.hue import *

bridge_ip_address = '192.168.0.2'
lamp_name='Cornerlight'

print("Initing the Hue bridge and light")

bridge = Bridge(bridge_ip_address)
api = bridge.get_api()
bridge.set_light(lamp_name, PARAM_TURNEDON, True)
bridge.set_light(lamp_name, PARAM_HUE, 65535)
bridge.set_light(lamp_name, PARAM_SATURATION, 0)
bridge.set_light(lamp_name, PARAM_BRIGHTNESS, 0)
bridge.set_light(lamp_name, PARAM_EFFECT, 'none') # colorloop or none supported

print("Initing the mindwave device at /dev/tty.MindWaveMobile-DevA")

headset = Headset('/dev/tty.MindWaveMobile-DevA')
time.sleep(2)

print("Init successful, starting the Illithid loop")

while True:
    print (f'Attention: {headset.attention}')
    if headset.attention > 60:
        print("Attentive, aren't you? Let's up the colors!")
        increase_intensity(bridge, lamp_name)
    else: 
        print("No attention, decreasing the intensity")
        decrease_intensity(bridge, lamp_name)
    time.sleep(2)


