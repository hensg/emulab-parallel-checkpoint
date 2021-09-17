#!/bin/bash

NUM_NODES=${1}
PORT=${2}

IP_OFFSET=${3}
# to avoid issues with x.x.x.1 ip address that may be used by another
# network device, we use an offset like 100 so the ip address list start
# from .100

for i in $(seq 0 $((NUM_NODES - 1))); do
    node_id=$((i+IP_OFFSET))
    sudo echo -e "${node_id} 10.1.1.${node_id} ${PORT}" >> /srv/config/hosts.config
done