# MidiHyperdeckBridge

This project aims to be the missing link between MIDI-Signals (i.e. from a Audio/MIDI-Backingtrack-Player) and the Hyperdeck API. It's build on top of the Blackmagic Design Hyperdeck WebUI example. It uses mido for MIDI-Parsing.

## Setup:

1) Connect a Blackmagic Design HyperDeck to your computer, via an Ethernet cable.
2) Adjust the App/SongMapping.py file to fullfill your needs (incoming MIDI commands to hyperdeck commands)
3) Go to App folder and run `python3 Main.py {hyperdeck ip address}` from your command line/terminal application.
4) Open `localhost:8080` in your chosen web browser to show the Web UI.

## Dependencies:

### Python

Python 3.6 or newer is required. On Debian systems, this can usually be installed via:
```
sudo apt install python3 python3-pip
```

### Python Libraries

1) [aiohttp](https://github.com/aio-libs/aiohttp) to provide the Websocket and asychronous HTTP library that communicates with the browser front-end.
2) [mido](https://mido.readthedocs.io/en/latest/) to read and parse from MIDI inputs
```
pip3 install aiohttp mido python-rtmidi
```
