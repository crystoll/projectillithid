import time
from playsound import playsound

from .mindwave.mindwave import Headset
from .hue.hue import *

bridge_ip_address = '192.168.0.2'
lamp_name='Effectlamp'

print("Initing the Hue bridge and light")

huecontroller = HueController(bridge_ip_address, lamp_name)
huecontroller.reset()
# bridge = Bridge(bridge_ip_address)
# api = bridge.get_api()
# bridge.set_light(lamp_name, PARAM_TURNEDON, True)
# bridge.set_light(lamp_name, PARAM_HUE, 65535)
# bridge.set_light(lamp_name, PARAM_SATURATION, 0)
# bridge.set_light(lamp_name, PARAM_BRIGHTNESS, 0)
# bridge.set_light(lamp_name, PARAM_EFFECT, 'none') # colorloop or none supported

print("Initing the mindwave device at /dev/tty.MindWaveMobile-DevA")

headset = Headset('/dev/tty.MindWaveMobile-DevA')
time.sleep(2)

print("Init successful, starting the Illithid loop")

while True:
    print (f'Attention: {headset.attention}')
    if headset.attention > 50:
        print("Attentive, aren't you? Let's up the colors!")
        huecontroller.increase_intensity()
        if huecontroller.intensity > 50:
            playsound('effect3.mp3')
    # else: 
        # print("No attention, decreasing the intensity")
        # huecontroller.decrease_intensity()
    print(f'Current intensity: {huecontroller.intensity}')

    time.sleep(1)


