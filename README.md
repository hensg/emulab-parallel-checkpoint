# emulab-parallel-checkpoint

## topology.py

The emulab main file used to create the topology dinamically.
There're some input parameters defined that can be fill out by the user when launch the topology.

## generate_config_hosts.sh

The system requires a set of defined IP and port addresses to work properly.
The number of nodes typed in the emulab's input parameter will be used to generate the `/srv/config/hosts.config` file.

## generate_system_config_initial_view.sh

The system requires some configurations related to view states, number of machines executing the consensus algorithm and so on.
The script takes the number of nodes and the node offset to dynamically generate the `/srv/config/system.config` file.


## install_service.sh

It dynamically creates a service using systemd file replacing the system parameters with the input parameters typed in emulab interface.


## SystemD commands

`sudo service bft-smart status`

`sudo service bft-smart stop`

`sudo service bft-smart start`

## JournalCTL commands
Useful to see service logs

`sudo journalctl -u bft-smart -f`

-f = follows, keep printing new incomming logs.
