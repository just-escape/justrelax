#!/bin/bash
export DISPLAY=:0;chromium --kiosk --app="http://localhost:8083?ws_url=d2broker.justescape%3A3032&channel_prefix=d2&chambers_version=2" --window-position=4920,0 --noerrdialogs --user-data-dir=/home/justescape/root_server/chrome-data-dir --password-store=basic --autoplay-policy=no-user-gesture-required --disable-features=Translate --disable-pinch
