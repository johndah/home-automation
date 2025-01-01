#!/bin/bash
docker pull homeassistant/home-assistant:latest
docker run -d --name="home-assistant" -p 8123:8123 --restart unless-stopped -v ~/git/home-automation:/config -v /etc/localtime:/etc/localtime:ro -v /run/dbus:/run/dbus:ro --net=host homeassistant/home-assistant:latest
