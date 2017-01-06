#!/bin/sh
echo "start"
echo "stop mopidy and sleep 3sec"
sudo systemctl stop mopidy &
echo 3
sleep 1
echo 2
sleep 1
echo 1
sleep 1
echo 0
echo "kill mopdidy"
sudo pkill -9 mopidy
# cd /home/pi/mopidy
# git pull
# pip install . -U
# apt-get update
# apt-get -y upgrade
echo "start mopidy"
sudo systemctl start mopidy
echo "done"
