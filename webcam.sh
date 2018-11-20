#!/bin/bash
DATE=$(date +"%Y-%m-%d_%H:%M:%S")
fswebcam -r 960x720 /home/pi/webcam/$DATE.jpg
cp /home/pi/webcam/$DATE.jpg /mnt/yandex.disk/webcam/
