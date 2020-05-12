from __future__ import print_function

import select
import serial
import threading
from pprint import pprint
import time
import datetime
import os
import struct

# Byte codes
CONNECT = b'\xc0'
DISCONNECT = b'\xc1'
AUTOCONNECT = b'\xc2'
SYNC = b'\xaa'
EXCODE = b'\x55'
POOR_SIGNAL = b'\x02'
ATTENTION = b'\x04'
MEDITATION = b'\x05'
BLINK = b'\x16'
HEADSET_CONNECTED = b'\xd0'
HEADSET_NOT_FOUND = b'\xd1'
HEADSET_DISCONNECTED = b'\xd2'
REQUEST_DENIED = b'\xd3'
STANDBY_SCAN = b'\xd4'
RAW_VALUE = b'\x80'
ASIC_EEG_POWER = b'\x83'

# Status codes
STATUS_CONNECTED = 'connected'
STATUS_SCANNING = 'scanning'
STATUS_STANDBY = 'standby'

class Headset(object):
    """
    A MindWave Headset
    """

    class DongleListener(threading.Thread):
        """
        Serial listener for dongle device.
        """

        def __init__(self, headset, *args, **kwargs):
            """Set up the listener device."""
            self.headset = headset
            self.counter = 0
            super(Headset.DongleListener, self).__init__(*args, **kwargs)

        def run(self):
            """Run the listener thread."""
            s = self.headset.dongle

            self.headset.running = True

            # Re-apply settings to ensure packet stream
            s.write(DISCONNECT)
            d = s.getSettingsDict()
            for i in range(2):
                d['rtscts'] = not d['rtscts']
                s.applySettingsDict(d)

            while self.headset.running:
                # Begin listening for packets
                try:
                    if s.read() == SYNC and s.read() == SYNC:
                        # Packet found, determine plength
                        while True:
                            plength = int.from_bytes(s.read(), byteorder='big')
                            if plength != 170:
                                break
                        if plength > 170:
                            continue

                        # Read in the payload
                        payload = s.read(plength)

                        # Verify its checksum
                        val = sum(b for b in payload[:-1])
                        val &= 0xff
                        val = ~val & 0xff
                        chksum = int.from_bytes(s.read(), byteorder='big')

                        # if val == chksum:
                        if True:  # ignore bad checksums
                            self.parse_payload(payload)
                except serial.SerialException:
                    break
                except (select.error, OSError):
                    break

            print('Closing connection...')
            if s and s.isOpen():
                s.close()

        def parse_payload(self, payload):
            """Parse the payload to determine an action."""
            while payload:
                # Parse data row
                excode = 0
                try:
                    code, payload = payload[0], payload[1:]
                    code_char = struct.pack('B',code)
                    self.headset.count = self.counter
                    self.counter = self.counter + 1
                    if (self.counter >= 100):
                        self.counter = 0
                except IndexError:
                    pass
                while code_char == EXCODE:
                    print('Excode bytes found')
                    # Count excode bytes
                    excode += 1
                    try:
                        code, payload = payload[0], payload[1:]
                    except IndexError:
                        pass
                if code < 0x80:
                    # This is a single-byte code
                    try:
                        value, payload = payload[0], payload[1:]
                    except IndexError:
                        pass
                    if code_char == POOR_SIGNAL:
                        # Poor signal
                        old_poor_signal = self.headset.poor_signal
                        self.headset.poor_signal = value
                        if self.headset.poor_signal > 0:
                            if old_poor_signal == 0:
                                for handler in \
                                        self.headset.poor_signal_handlers:
                                    handler(self.headset,
                                            self.headset.poor_signal)
                        else:
                            if old_poor_signal > 0:
                                for handler in \
                                        self.headset.good_signal_handlers:
                                    handler(self.headset,
                                            self.headset.poor_signal)
                    elif code_char == ATTENTION:
                        # Attention level
                        self.headset.attention = value
                        for handler in self.headset.attention_handlers:
                            handler(self.headset, self.headset.attention)
                    elif code_char == MEDITATION:
                        # Meditation level
                        self.headset.meditation = value
                        for handler in self.headset.meditation_handlers:
                            handler(self.headset, self.headset.meditation)
                    elif code_char == BLINK:
                        # Blink strength
                        self.headset.blink = value
                        for handler in self.headset.blink_handlers:
                            handler(self.headset, self.headset.blink)
                else:
                    # This is a multi-byte code
                    try:
                        vlength, payload = payload[0], payload[1:]
                    except IndexError:
                        continue
                    value, payload = payload[:vlength], payload[vlength:]

                    if code_char == RAW_VALUE and len(value) >= 2:
                        raw = value[0]*256+value[1]
                        if (raw >= 32768):
                            raw = raw-65536
                        self.headset.raw_value = raw
                        for handler in self.headset.raw_value_handlers:
                            handler(self.headset, self.headset.raw_value)
                    if code_char == HEADSET_CONNECTED:
                        # Headset connect success
                        run_handlers = self.headset.status != STATUS_CONNECTED
                        self.headset.status = STATUS_CONNECTED
                        self.headset.headset_id = value.encode('hex')
                        if run_handlers:
                            for handler in \
                                    self.headset.headset_connected_handlers:
                                handler(self.headset)
                    elif code_char == HEADSET_NOT_FOUND:
                        # Headset not found
                        if vlength > 0:
                            not_found_id = value.encode('hex')
                            for handler in \
                                    self.headset.headset_notfound_handlers:
                                handler(self.headset, not_found_id)
                        else:
                            for handler in \
                                    self.headset.headset_notfound_handlers:
                                handler(self.headset, None)
                    elif code_char == HEADSET_DISCONNECTED:
                        # Headset disconnected
                        headset_id = value.encode('hex')
                        for handler in \
                                self.headset.headset_disconnected_handlers:
                            handler(self.headset, headset_id)
                    elif code_char == REQUEST_DENIED:
                        # Request denied
                        for handler in self.headset.request_denied_handlers:
                            handler(self.headset)
                    elif code_char == STANDBY_SCAN:
                        # Standby/Scan mode
                        try:
                            byte = value[0]
                        except IndexError:
                            byte = None
                        if byte:
                            run_handlers = (self.headset.status !=
                                            STATUS_SCANNING)
                            self.headset.status = STATUS_SCANNING
                            if run_handlers:
                                for handler in self.headset.scanning_handlers:
                                    handler(self.headset)
                        else:
                            run_handlers = (self.headset.status !=
                                            STATUS_STANDBY)
                            self.headset.status = STATUS_STANDBY
                            if run_handlers:
                                for handler in self.headset.standby_handlers:
                                    handler(self.headset)
                    elif code_char == ASIC_EEG_POWER:
                        j = 0
                        for i in ['delta', 'theta', 'low-alpha', 'high-alpha', 'low-beta', 'high-beta', 'low-gamma', 'mid-gamma']:
                            self.headset.waves[i] = value[j]*255*255+value[j+1]*255+value[j+2]
                            j += 3
                        for handler in self.headset.waves_handlers:
                            handler(self.headset, self.headset.waves)

    def __init__(self, device, headset_id=None, open_serial=True):
        """Initialize the  headset."""
        # Initialize headset values
        self.dongle = None
        self.listener = None
        self.device = device
        self.headset_id = headset_id
        self.poor_signal = 255
        self.attention = 0
        self.meditation = 0
        self.blink = 0
        self.raw_value = 0
        self.waves = {}
        self.status = None
        self.count = 0
        self.running = False

        # Create event handler lists
        self.poor_signal_handlers = []
        self.good_signal_handlers = []
        self.attention_handlers = []
        self.meditation_handlers = []
        self.blink_handlers = []
        self.raw_value_handlers = []
        self.waves_handlers = []
        self.headset_connected_handlers = []
        self.headset_notfound_handlers = []
        self.headset_disconnected_handlers = []
        self.request_denied_handlers = []
        self.scanning_handlers = []
        self.standby_handlers = []

        # Open the socket
        if open_serial:
            self.serial_open()

    def serial_open(self):
        """Open the serial connection and begin listening for data."""
        if not self.dongle or not self.dongle.isOpen():
            self.dongle = serial.Serial(self.device, 115200)

        if not self.listener or not self.listener.isAlive():
            self.listener = self.DongleListener(self)
            self.listener.daemon = True
            self.listener.start()

    def serial_close(self):
        """Close the serial connection."""
        self.dongle.close()

    def stop(self):
        self.running = False
