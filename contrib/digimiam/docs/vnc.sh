xrandr --listactivemonitors|awk -- 'BEGIN { getline } { gsub(/\/[[:digit:]]+/,"",$3) ; print $3 }'

x11vnc -rfbauth ~/.vnc/passwd -forever -rfbport 5900
x11vnc -clip 1920x1080+1080+0 -rfbauth ~/.vnc/passwd -forever -rfbport 5901
x11vnc -clip 1920x1080+3000+0 -rfbauth ~/.vnc/passwd -forever -rfbport 5902
x11vnc -clip 1080x1920+0+0 -rfbauth ~/.vnc/passwd -forever -rfbport 5903
x11vnc -clip 1920x1080+4920+0 -rfbauth ~/.vnc/passwd -forever -rfbport 5904
