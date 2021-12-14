#!/bin/bash
export DISPLAY=:0;chromium --kiosk --app="http://localhost:8081?ws_url=d1broker.justescape%3A3032&channel_prefix=d1&ventilation_button_offset=1" --window-position=3000,0 --noerrdialogs --user-data-dir=/home/justescape/orders/chrome-data-dir --password-store=basic --autoplay-policy=no-user-gesture-required --disable-features=Translate --disable-pinch
