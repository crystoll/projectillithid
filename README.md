# Project Illithid

This is a Python project for using MindWave EEG Headset. This is based on Python2 code from https://github.com/faturita/python-mindwave, ported from Python2 to Python3 for convenience, with some fixes in the codebase as well. I used Faturita fork because it had support for reading waves directly from the headset, unlike the original BarkleyUS fork. 

For this to work, you need to have suitable libraries installed (pyserial), and you need to have Mindwave bluetooth headset paired with your machine. You do not need to have separate connect/disconnect cycle with Mindwave Mobile.


## How to use this?

Very simple. You need Python 3, and Mindwave Mobile. You also need to be prepared to sort out some bluetooth related stuff, for example bluetooth connectivity may require various libs and dependencies depending on which OS(+version) you are running, connection to device is done differently on MacOS and Win, etc. It's a hot steaming mess. But others have managed to do it, so help yourself and see if you can make it run.

## recorder

Recorder is a simple Python script that is interactive. It will ask you some details for filename, and then sample your brain every .5 seconds until 10 minutes recording has been done. Resulting .dat files may then be analyzed using  ..

There's also test.py for simpler testing that everything works. mindwave.py is the actual library fork.

## ProjectIllithid

There's a sample Jupyter notebook that runs on Python 3 and contains some experiments on visualizing your brain internals. Feel free to use it as a starting place.

