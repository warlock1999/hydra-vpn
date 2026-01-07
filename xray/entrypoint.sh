#!/bin/sh
# Inject UUID
sed -i "s/UUID-PLACEHOLDER/$HYDRA_UUID/g" /etc/xray/config.json

# Start Xray
/usr/bin/xray -config /etc/xray/config.json
