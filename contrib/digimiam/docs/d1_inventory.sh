#!/bin/bash
export DISPLAY=:0;chromium --kiosk --app="http://localhost:8082?ws_url=d1broker.justescape%3A3032&channel_prefix=d1" --window-position=0,0 --noerrdialogs --user-data-dir=/home/justescape/inventory/chrome-data-dir --password-store=basic --autoplay-policy=no-user-gesture-required --disable-features=Translate --disable-pinch
