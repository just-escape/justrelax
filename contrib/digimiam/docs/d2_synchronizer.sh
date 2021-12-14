#!/bin/bash
# --window-size=1920,1040 because otherwise the 40px height application panel on the bottom of the screen
# is identified as a blocker for the fullscreen mode to happen at the desired screen position 
export DISPLAY=:0;chromium --kiosk --app="http://localhost:8080?ws_url=d2broker.justescape%3A3032&channel_prefix=d2&light_map_version=2" --window-size=1920,1040 --noerrdialogs --user-data-dir=/home/justescape/synchronizer/chrome-data-dir --password-store=basic --autoplay-policy=no-user-gesture-required --disable-features=Translate --disable-pinch
