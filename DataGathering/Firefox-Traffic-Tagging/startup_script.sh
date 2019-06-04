#!/bin/bash

Xvnc :0 -rfbauth /mypass -geometry 1280x720 -depth 16 &
export DISPLAY=:0
sleep 5
jwm &
sleep 5
firefox
bash
