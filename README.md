# Lobe

![Lobe Logo](logo-with-text.svg)  
This is a Home Assistant custom component for [Lobe](lobe.ai). Lobe is an AI tool that can classify images.
This component lets you easily use an exported model along with another server to classify a camera entity's feed with it.

# Installation

Use HACS for the integration. You'll also need a seperate server. Steps to install on another server:

- Install the [Lobe](https://github.com/lobe/lobe-python#linux) library.
- Install Flask.
- Export a Tensorflow Lite model into a folder on the server.
- Copy over [app.py](app.py) and change the folder location.
- Run app.py.
- You'll probably want to [make it run on start](https://stackoverflow.com/questions/57031864/running-flask-app-automatically-after-boot-does-not-work-correctly).

# Configuration

This is the configuration format:

```yaml
image_processing:
  - platform: lobe
    entity_id: camera.front_door_livestream # Camera entity ID
    name: "Front Door Status" # Optional; Custom name
    server: "http://lobeserver.local:5623" # Server address
    scan_interval: 2 # Optional; How often to update
```

It will produce an entity something like this:
![image](https://user-images.githubusercontent.com/10727862/116791937-70c6c300-aa72-11eb-9821-975b9d9bbaee.png)
