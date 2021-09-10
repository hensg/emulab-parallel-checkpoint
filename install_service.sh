#!/bin/bash

ENV_FILE_PATH=/srv/emulab/bft-smart.env

sed -i 's/NODE_ID=/NODE_ID=${1}/g' $ENV_FILE_PATH
sed -i 's/INTERVAL=/INTERVAL=${2}/g' $ENV_FILE_PATH
sed -i 's/THREADS=/THREADS=${3}/g' $ENV_FILE_PATH
sed -i 's/INITIAL_ENTRIES=/INITIAL_ENTRIES=${4}/g' $ENV_FILE_PATH
sed -i 's/CHECKPOINT_INTERVAL=/CHECKPOINT_INTERVAL=${5}/g' $ENV_FILE_PATH
sed -i 's/PARALLEL=/PARALLEL=${6}/g' $ENV_FILE_PATH

sudo mv /srv/emulab/bft-smart.service /etc/systemd/system/

systemctl enable bft-smart
systemctl start bft-smart