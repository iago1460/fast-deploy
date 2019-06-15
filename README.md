# Fast Deploy

Setup and deploy projects through docker in the Raspberry Pi.

Specifically this guide sets up a [Duck DNS](https://www.duckdns.org) domain over HTTPS 
running [Home Assistant](https://www.home-assistant.io) secured with [Fail2ban](https://www.fail2ban.org)

## Content

This setup includes:

* [Traefik](https://traefik.io/) - The Cloud Native Edge Router.
* [Let’s Encrypt](https://letsencrypt.org) - Let’s Encrypt is a free, automated, and open Certificate Authority.
* [Duck DNS](https://www.duckdns.org) - Duck DNS free dynamic DNS hosted on Amazon VPC.
* [Fail2ban](https://www.fail2ban.org) - Fail2ban scans log files and bans IPs that show the malicious signs.
* [Eclipse Mosquitto](https://mosquitto.org) - Eclipse Mosquitto is an open source message broker that implements the MQTT protocol.
* [Home Assistant](https://www.home-assistant.io) - Open source home automation that puts local control and privacy first.
* [deCONZ](https://hub.docker.com/r/marthoc/deconz/) - deCONZ is a software that communicates with Conbee/Raspbee Zigbee gateways and exposes Zigbee devices that are connected to the gateway.


## Requirements

Linux / Mac OS

* `wget`
* `unzip`
* `rsync`
* `docker`


## Installation Guide

1 Lets start creating a environment variables file

    cp .sample.env .env

2 Open `.env` and fill `REPLACE_ME` with your data and **save the file**.

2 Evaluate the environment variables file:

    source .env

3 Give execution permissions to the `setup` script:

    chmod +x setup

4 Download additional resources

    ./setup init

5 After running a new folder called `config` should have been created.

6 Insert a micro sd

7 Flash the sd card choosing one of the following commands

    ./setup flash_sd

    ./setup flash_sd_wifi

8 Put the micro sd in and boot the system.


### Last steps

Once the system is up, send the config through ssh:

    ./setup export_config
    
Let's connect to the pi and run the system:
    
    ssh pirate@${HOSTNAME}.local
    
    cd workspace
    source .env
    docker-compose up -d

Once all works, import the config from rpi and store it in a save place
    
    ./setup import_config


## Disclaimer

This repository is heavily based on the following work:
 
 * [HypriotOS](https://github.com/hypriot/image-builder-rpi) - HypriotOS is the fastest way to get Docker up and running on the Raspberry Pi. Download - Flash - Boot - Done.
 * [flash](https://github.com/hypriot/flash) - Command line script to flash SD card images of any kind.
 * [Configurer](https://github.com/iago1460/configurer) - A config render tool using based on Jinja template variables.

