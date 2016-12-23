#!/bin/sh

sudo systemctl stop mopidy &&
sleep 3 &&
sudo pkill -9 mopidy &&
sudo systemctl restart mopidy
