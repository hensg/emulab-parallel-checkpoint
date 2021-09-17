#!/bin/bash

NUM_NODES=${1}
NODE_OFFSET=${2}

list_of_nodes=`seq -s, ${NODE_OFFSET} $((NODE_OFFSET + NUM_NODES - 1))`

sudo sed -i "s/system\.initial\.view.*/system\.initial\.view=${list_of_nodes}/g" /srv/config/system.config
sudo sed -i "s/system\.servers\.num.*/system\.servers\.num=${NUM_NODES}/g" /srv/config/system.config
sudo sed -i "s/system\.servers\.f.*/system\.servers\.f=$(((NUM_NODES - 1) / 2))/g" /srv/config/system.config