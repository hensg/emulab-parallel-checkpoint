"""A cluster node topology for testing bft-smart with parallel checkpointing.

The project source code is in /srv/EMULAB-RND/

Instructions:
After machine starts, a script to mount the disks will run and you can start
the bft-smart checkpointing experiments.
"""

# Import the Portal object.
import geni.portal as portal
# Import the Emulab specific extensions.
import geni.rspec.emulab as emulab
# Import the ProtoGENI library.
import geni.rspec.pg as pg

# Create a portal object,
pc = portal.Context()

# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()
request.setRoutingStyle('static')

portal.context.defineParameter("u", "Your emulab username", portal.ParameterType.STRING, 'hensg')
portal.context.defineParameter("n", "Number of machines", portal.ParameterType.INTEGER, 4)
portal.context.defineParameter("t", "Type of machines", portal.ParameterType.STRING, 'd430')
portal.context.defineParameter("ri", "Report Interval", portal.ParameterType.INTEGER, 1)
portal.context.defineParameter("th", "Number of threads", portal.ParameterType.INTEGER, 4)
portal.context.defineParameter("ie", "Number of initial entries in size (MB)", portal.ParameterType.INTEGER, 1024)
portal.context.defineParameter("ci", "Checkpoint interval in number of commands", portal.ParameterType.INTEGER, 50000)
portal.context.defineParameter("p", "Should use parallel checkpointing?", portal.ParameterType.BOOLEAN, False)

params = portal.context.bindParameters()


if params.n < 1 or params.n > 36:
    portal.context.reportError(portal.ParameterError("You must choose at least 1 and no more than 36 machines."))

allowed_types = ["d430","d820"]
if params.t not in allowed_types:
    portal.context.reportError(portal.ParameterError("You must choose one of this types: " + ",".join(allowed_types)))


# Link lan0
link_lan0 = request.LAN('lan0')
link_lan0.setNoBandwidthShaping()
link_lan0.trivial_ok = True

node_offset = 100
# to avoid issues with .1 ip address that may be used by another network device

def raw_machine(lan, node_name, node_id, node_ip, params, node_offset):
    node = request.RawPC(node_name)
    node.hardware_type = params.t
    node.disk_image = 'urn:publicid:IDN+emulab.net+image+ScalableSMR:parallel-checkpoint'
    iface = node.addInterface('eth0', pg.IPv4Address(node_ip, '255.255.255.0'))
    iface.bandwidth = 10000000
    lan.addInterface(iface)

    node.addService(pg.Install(url="https://github.com/hensg/emulab-parallel-checkpoint/releases/download/1.0/bft-smart.tar.gz", path="/srv"))
    node.addService(pg.Install(url="https://github.com/hensg/emulab-parallel-checkpoint/releases/download/1.0/emulab.tar.gz", path="/srv"))
    node.addService(pg.Execute(shell='bash', command='sudo /srv/emulab-parallel-checkpoint/mount_disks.sh'))
    node.addService(pg.Execute(shell='bash', command='sudo /srv/emulab-parallel-checkpoint/install_dependencies.sh'))
    node.addService(pg.Execute(shell='bash', command='sudo /srv/emulab-parallel-checkpoint/generate_config_hosts.sh {num_nodes} {port} {ip_offset}'.format(
        num_nodes=params.n,
        port=11000,
        ip_offset=node_offset
    )))

    node.addService(pg.Execute(shell='bash', command='sudo /srv/emulab-parallel-checkpoint/generate_system_config_initial_view.sh {num_nodes} {node_offset}'.format(
        num_nodes=params.n,
        node_offset=node_offset
    )))

    node.addService(pg.Execute(shell='bash', command='sudo rm /srv/config/currentView'))
    node.addService(pg.Execute(
        shell='bash',
        command='sudo /srv/emulab-parallel-checkpoint/install_service.sh {username} {id} {interval} {threads} {initial_entries} {checkpoint_interval} {parallel}'.format(
            username=params.u,
            id=node_id,
            interval=params.ri,
            threads=params.th,
            initial_entries=params.ie,
            checkpoint_interval=params.ci,
            parallel=params.p
    )))

for i in range(params.n):
    node_id = node_offset + i
    node_ip = '10.1.1.' + str(node_id)
    raw_machine(lan=link_lan0, node_name='node_' + str(node_id), node_id=node_id, node_ip=node_ip, params=params, node_offset=node_offset)

raw_machine(lan=link_lan0, node_name='client', node_id=255, node_ip='10.1.1.254', params=params, node_offset=node_offset)

# Print the generated rspec
pc.printRequestRSpec(request)
