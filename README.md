# Project Illithid

This is a Python project for using MindWave EEG Headset. This is based on Python2 code from https://github.com/faturita/python-mindwave, ported from Python2 to Python3 for convenience, with some fixes in the codebase as well. I used Faturita fork because it had support for reading waves directly from the headset, unlike the original BarkleyUS fork. 

For this to work, you need to have suitable libraries installed (pyserial), and you need to have Mindwave bluetooth headset paired with your machine. You do not need to have separate connect/disconnect cycle with Mindwave Mobile.


## How to use this?

Very simple. You need Python 3, and Mindwave Mobile. You also need to be prepared to sort out some bluetooth related stuff, for example bluetooth connectivity may require various libs and dependencies depending on which OS(+version) you are running, connection to device is done differently on MacOS and Win, etc. It's a hot steaming mess. But others have managed to do it, so help yourself and see if you can make it run.

## How is this structured?

We have two subfolders, mindreader, and huecontrol. 

mindreader contains simple code to connect to mindwave device, and read eeg values. There is also tool to record said data, as well as some python notebooks to analyze data or visualize real-time.

huecontrol combines this with Philips Hue lightbulb control code, by focusing your thoughts you can effect the light intensity.