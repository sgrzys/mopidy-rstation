#!/bin/sh

sudo systemctl restart mopidy &&
sleep 3 &&
sudo pkill -9 mopidy &&
sudo systemctl start mopidy
