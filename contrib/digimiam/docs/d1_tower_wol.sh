#!/bin/bash

# Installed on d1advertiser.justescape and d2advertiser.justescape

for i in {1..30}
do
  wakeonlan -i 172.16.255.255 a8:5e:45:11:65:9e
  if [ $? -eq 0 ]
  then
    break
  fi

  sleep 1
done
