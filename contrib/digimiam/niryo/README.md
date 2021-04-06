SSL is broken on the niryo SD card. So everything needs to be copied and cannot be downloaded from the
niryo itself (no git clone, no pip install).

On your workstation:
```
scp -r justrelax/contrib/digimiam niryo@w.x.y.z:~/justrelax_niryo
wget https://codeload.github.com/websocket-client/websocket-client/zip/refs/heads/master
unzip websocket-client-master.zip
scp -r websocket-client-master niryo@w.x.y.z:~
```

The yaml dependency is already installed on the SD card.

On the niryo SD card:

```
virtualenv venv_justrelax --system-site-packages
source venv_justrelax/bin/activate
cd websocket-client-master
python setup.py install
cd ../justrelax_niryo
python setup.py develop
```