"""A cluster node topology for testing bft-smart with parallel checkpointing.

The project source code is in /srv/EMULAB-RND/

Instructions:
After machine starts, a script to mount the disks will run and you can start
the bft-smart checkpointing experiments.
"""

# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as pg
# Import the Emulab specific extensions.
import geni.rspec.emulab as emulab

# Create a portal object,
pc = portal.Context()

# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()
request.setRoutingStyle('static')

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

for i in range(params.n):
    node = request.RawPC('Node'+str(i+1))
    node.hardware_type = params.t
    #node.disk_image = 'urn:publicid:IDN+emulab.net+image+ScalableSMR:BFT-SMaRt-PCheckpoint'
    iface = node.addInterface('eth0', pg.IPv4Address('10.1.1.'+str(i+2),'255.255.255.0'))
    iface.bandwidth = 10000000
    link_lan0.addInterface(iface)

    node.addService(pg.Install(url="https://github.com/hensg/emulab/releases/download/1.0-SNAPSHOT/bft-smart.tar.gz", path="/srv"))
    node.addService(pg.Install(url="https://github.com/hensg/emulab/releases/download/1.0-SNAPSHOT/emulab.tar.gz", path="/srv"))
    node.addService(pg.Execute(shell='bash', command='sudo /srv/emulab/mount_disks.sh'))
    node.addService(pg.Execute(shell='bash', command='sudo /srv/emulab/install_dependencies.sh'))
    node.addService(pg.Execute(shell='bash', command='sudo /srv/emulab/install_service.sh'))

    cmd = 'sudo /srv/install_service.sh {id} {interval} {threads} {initial_entries} {checkpoint_interval} {parallel}'.format(
        id=(i+1),
        interval=params.ri,
        threads=params.th,
        initial_entries=params.ie,
        checkpoint_interval=params.ci,
        parallel=params.p
    )
    node.addService(pg.Execute(shell='bash', command=cmd))


# Print the generated rspec
pc.printRequestRSpec(request)
