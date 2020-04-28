# Huecontrol ffor controlling Hue with your mind

## Getting started

You need Python 3.7 or later, preferable with virtual env. For example:

```
python3 -m venv venv
source venv/bin/activate
```

To install dependencies:

````
pip install -r requirements.txt
````

To run the app:

python control_hue.py

To stop the session:

```
deactivate
```

## How to use

https://github.com/studioimaginaire/phue

You need to change the ip address in control_hue.py file to match the ip address of your hue bridge.
You should also adjust light settings to match your own setup.
Note to self: Disable VPN when trying this, it's capturing ip ranges.
To run the app, you need to press the link button once within 30 seconds time before running the app.

## Debugging

WARNING: pip is configured with locations that require TLS/SSL, however the ssl module in Python is not available.

Root cause: Multitude of options here, depending on which OS and how it's set up. I found enlightenment for OSX as follows:

```
brew uninstall python
rm -rf $(pyenv root)
brew uninstall pyenv-virtualenv   
brew uninstall pyenv
brew install pyenv pyenv-virtualenv
pyenv install 3.7.7
pyenv install 3.8.2
pyenv global 3.8.2
```

