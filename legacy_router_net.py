from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

def myNetwork():
    # We create a base IP address with the subnet of 8 to declare the network length(8) and host length (24) 
    net = Mininet( topo=None, build=False, ipBase='10.0.0.0/8' )

    info( '*** Adding controller\n' )
    info( '*** Add switches\n')
    # Because the network portion of the IP address is only the first 8, we can arbitrarlity put whatever numbers we want for the host length. Ex. Network is 10, host is 123.123.123
    r1 = net.addHost('r1', cls=Node, ip='10.123.123.123')
    r1.cmd('sysctl -w net.ipv4.ip_forward=1')

    info( '*** Add hosts\n')
    #We need to change the IP addresses to make them distinct.
    #We also needed to tell the host directly which route to go to.
    # We also changed defaultRoute=none to defaultRoute='(ip address)'
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute='via 10.123.123.123')
    h1 = net.addHost('h1', cls=Host, ip='172.16.0.100', defaultRoute='via 172.16.1.100')

    info( '*** Add links\n')
    #Each link needs a source node, destination node, source port, destination port
    net.addLink(h2, r1, intfName2='r0-eth0', params2={'ip':'10.123.123.123/8'})
    net.addLink(h1, r1, intfName2='r0-eth1', params2={'ip':'172.16.1.100/8'})

    info( '*** Starting network\n')
    net.build()
    
    # We did not need any controlllers, switches, and any 'post configure switches and hosts' 

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()
