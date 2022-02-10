#!/bin/bash
set -x
disks=`lsblk | grep ^sd | grep -v sda | awk '{print $1}'`

i=0

for disk in $disks
do
    echo "Mounting disk $disk at /disk$i"
    sudo mkdir -p /disk$i/checkpoint$i/
    sudo chmod 777 /disk$i/checkpoint$i/
    sudo mkfs.ext4 /dev/$disk
    sudo mount /dev/$disk /disk$i
    sudo mkdir -p /disk$i/checkpoint$i/states/
    sudo mkdir -p /disk$i/checkpoint$i/metadata/
    sudo chmod 777 -R /disk$i/checkpoint$i/
    i=$((i+1))
done
