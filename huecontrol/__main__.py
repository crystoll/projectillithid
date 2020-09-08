import time
from playsound import playsound

from .mindwave.mindwave import Headset
from .hue.hue import *

bridge_ip_address = '192.168.0.2'
lamp_name='Effectlamp'

print("Initing the Hue bridge and light")

huecontroller = HueController(bridge_ip_address)
huecontroller.reset()

print("Initing the mindwave device at /dev/tty.MindWaveMobile-DevA")

headset = Headset('/dev/tty.MindWaveMobile-DevA')
time.sleep(2)

print("Init successful, starting the Illithid loop")

while True:
    print (f'Attention: {headset.attention}')
    if headset.attention > 50:
        print("Attentive, aren't you? Let's up the intensity!")
        huecontroller.increase_intensity()
    print(f'Current intensity: {huecontroller.intensity}')

    time.sleep(1)


