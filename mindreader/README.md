## recorder

Recorder is a simple Python script that is interactive. It will ask you some details for filename, and then sample your brain every .5 seconds until 10 minutes recording has been done. Resulting .dat files may then be analyzed using  ..

There's also test.py for simpler testing that everything works. mindwave.py is the actual library fork.

## ProjectIllithid

There's a sample Jupyter notebook that runs on Python 3 and contains some experiments on visualizing your brain internals. Feel free to use it as a starting place.

## Requirements

python3 -m pip install pyserial

python3 -m pip install jupyter

## Debugging

Got a device busy error? Check that 

- Bluetooth is on in laptop
- Device is on
- Device has been paired with your laptop
- You can see a /dev/tty.MindWaveMobile-DevA device (on Mac)

Missing AppKit? Do a:

python3 -m pip install pyobjc
