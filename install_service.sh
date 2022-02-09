#!/bin/bash

set -x
set -v

USERNAME=${1}
NODE_ID=${2}
INTERVAL=${3}
THREADS=${4}
INITIAL_ENTRIES=${5}
CHECKPOINT_INTERVAL=${6}
PARALLEL=${7}

# create logging directory
sudo mkdir -p /var/log/bft-smart/
sudo chmod 777 /var/log/bft-smart
sudo chown -R $USERNAME /var/log/bft-smart
sudo chown -R $USERNAME /srv/

ENV_FILE_PATH=/srv/emulab-parallel-checkpoint/bft-smart.service

sudo sed -i "s/=NODE_ID=/=NODE_ID=${NODE_ID}/g" $ENV_FILE_PATH
sudo sed -i "s/=INTERVAL=/=INTERVAL=${INTERVAL}/g" $ENV_FILE_PATH
sudo sed -i "s/=THREADS=/=THREADS=${THREADS}/g" $ENV_FILE_PATH
sudo sed -i "s/=INITIAL_ENTRIES=/=INITIAL_ENTRIES=${INITIAL_ENTRIES}/g" $ENV_FILE_PATH
sudo sed -i "s/=CHECKPOINT_INTERVAL=/=CHECKPOINT_INTERVAL=${CHECKPOINT_INTERVAL}/g" $ENV_FILE_PATH
sudo sed -i "s/=PARALLEL=/=PARALLEL=${PARALLEL}/g" $ENV_FILE_PATH

sudo mv /srv/emulab-parallel-checkpoint/bft-smart.service /etc/systemd/system/

systemctl enable bft-smart
systemctl start bft-smart
