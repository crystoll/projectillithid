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

class HueController(object):
    """
    Hue controller
    """

    def __init__(self, ip_address, lamp_name, *args, **kwargs):
        self.bridge = Bridge(ip_address)
        self.api = self.bridge.get_api()
        self.lamp_name = lamp_name
        self.intensity = 0

    def reset(self):
        """
        Reset lamp to 0, white, no effect
        """
        self.bridge.set_light(self.lamp_name, PARAM_TURNEDON, True)
        self.bridge.set_light(self.lamp_name, PARAM_HUE, 65535)
        self.bridge.set_light(self.lamp_name, PARAM_SATURATION, 0)
        self.bridge.set_light(self.lamp_name, PARAM_BRIGHTNESS, 0)
        self.bridge.set_light(self.lamp_name, PARAM_EFFECT, 'none') # colorloop or none supported


    def get_light_ids(self):
        lights_info = self.api['lights']
        lamp_ids = [int(key) for key, value in lights_info.items()]
        return lamp_ids


    def get_light_names(self):
        lights_info = self.api['lights']
        lamp_names = [value['name'] for key, value in lights_info.items()]
        return lamp_names

    def update_state(self):
        print(f'Using intensity {self.intensity} and value {round(254/100*self.intensity)}')
        self.bridge.set_light(self.lamp_name, PARAM_SATURATION, round(254/100*self.intensity))
        if (self.intensity == 100):
            self.bridge.set_light(self.lamp_name, PARAM_BRIGHTNESS,0, transitiontime=0.5)
            self.bridge.set_light(self.lamp_name, PARAM_BRIGHTNESS, 254, transitiontime=0.5)
        else:
            self.bridge.set_light(self.lamp_name, PARAM_BRIGHTNESS,round(254/100*self.intensity)) 

    def increase_intensity(self):
        if self.intensity < 100:
            self.intensity = self.intensity + 5
        self.update_state()


    def decrease_intensity(self):
        if self.intensity > 1:
            self.intensity = self.intensity - 5
        self.update_state()



