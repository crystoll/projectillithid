import mindwave, time

headset = mindwave.Headset('/dev/tty.MindWaveMobile-DevA')
#headset = mindwave.Headset('COM4')
time.sleep(2)

while True:
    time.sleep(.5)
    print ("Raw value: %s, Attention: %s, Meditation: %s" % (headset.raw_value, headset.attention, headset.meditation))
    print ("Waves: {}".format(headset.waves))