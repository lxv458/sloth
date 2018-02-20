import logging
import latency
import time
import os

import utils
from tests.network import Network
from tests.router import Router
from tests.subnet import Subnet
from tests.port import Port
from tests.trunk import Trunk
from tests.bgpvpn import Bgpvpn
from tests.firewall import Firewall
from tests.firewallpolicy import FirewallPolicy
from tests.firewallrule import FirewallRule
from tests.floatingip import FloatingIP
from tests.gateway import Gateway
from tests.gatewayconnection import GatewayConnection
from tests.loadbalancer import Loadbalancer
from tests.loadbalancerhealthmonitor import LoadbalancerHealthMonitor
from tests.loadbalancerlistener import LoadbalancerListener
from tests.loadbalancerpool import LoadbalancerPool
from tests.meteringlabel import MeteringLabel
from tests.meteringrule import MeteringLabelRule
from tests.qospolicy import QosPolicy
from tests.vpnservice import VpnService
# from tests.securitygroup import SecurityGroup
from tests.securitygrouprule import SecurityGroupRule
from tests.sfcflowclassifier import SFCFlowClassifier
from tests.sfcportchain import SFCPortChain
from tests.sfcportpair import SFCPortPair
from tests.sfcportpairgroup import SFCPortPairGroup

if __name__ == '__main__':

    logging_config = utils.get_logging_config('logging')
    filename = logging_config['filename']

    if os.path.exists(filename):
        os.remove(filename)

    logging.basicConfig(filename=filename, level=logging_config['level'])

    for i in range(200):
        print('Test Round ' + str(i) + ' ' + time.strftime('%Y-%m-%d', time.localtime(time.time())))
        logging.info('Test Round ' + str(i) + ' ' + time.strftime('%Y-%m-%d', time.localtime(time.time())))

        # Network.perform_tests('server', 'admin')
        # Router.perform_tests('server', 'admin')
        # Subnet.perform_tests('server', 'admin')
        # Port.perform_tests('server', 'admin')
        # # Trunk.perform_tests('server', 'Gary')
        # Bgpvpn.perform_tests('server', 'admin')
        # Firewall.perform_tests('server', 'admin')
        # FirewallPolicy.perform_tests('server', 'admin')
        # FirewallRule.perform_tests('server', 'admin')
        # FloatingIP.perform_tests('server', 'admin')
        # Gateway.perform_tests('server', 'admin')
        # GatewayConnection.perform_tests('server', 'admin')
        # Loadbalancer.perform_tests('server', 'admin')
        # LoadbalancerHealthMonitor.perform_tests('server', 'admin')
        # LoadbalancerListener.perform_tests('server', 'admin')
        # LoadbalancerPool.perform_tests('server', 'admin')
        # MeteringLabel.perform_tests('server', 'admin')
        # MeteringLabelRule.perform_tests('server', 'admin')
        # QosPolicy.perform_tests('server', 'admin')
        # VpnService.perform_tests('server', 'admin')
        # # SecurityGroup.perform_tests('server', 'admin')
        # SecurityGroupRule.perform_tests('server', 'admin')
        # SFCFlowClassifier.perform_tests('server', 'admin')
        # SFCPortChain.perform_tests('server', 'admin')
        # SFCPortPair.perform_tests('server', 'admin')
        # SFCPortPairGroup.perform_tests('server', 'admin')

        # Network.perform_tests('server', 'Lily')
        # Network.perform_tests('server', 'admin')
        # Router.perform_tests('server', 'Lily')
        # Subnet.perform_tests('server', 'Tom')
        # Port.perform_tests('server', 'Tom')
        # Trunk.perform_tests('server', 'Gary')
        # Bgpvpn.perform_tests('server', 'Gary')
        # Firewall.perform_tests('server', 'Tom')
        # FirewallPolicy.perform_tests('server', 'Tom')
        # FirewallRule.perform_tests('server', 'Tom')
        # FloatingIP.perform_tests('server', 'Gary')
        # Gateway.perform_tests('server', 'admin')
        # GatewayConnection.perform_tests('server', 'admin')
        # Loadbalancer.perform_tests('server', 'Gary')
        # LoadbalancerHealthMonitor.perform_tests('server', 'Tom')
        # LoadbalancerListener.perform_tests('server', 'Jack')
        # LoadbalancerPool.perform_tests('server', 'admin')
        # MeteringLabel.perform_tests('server', 'Gary')
        # MeteringLabelRule.perform_tests('server', 'Tom')
        # QosPolicy.perform_tests('server', 'Tom')
        # VpnService.perform_tests('server', 'admin')
        # # SecurityGroup.perform_tests('server', 'admin')
        # SecurityGroupRule.perform_tests('server', 'Gary')
        # SFCFlowClassifier.perform_tests('server', 'admin')
        # SFCPortChain.perform_tests('server', 'admin')
        # SFCPortPair.perform_tests('server', 'admin')
        # SFCPortPairGroup.perform_tests('server', 'admin')

        Network.perform_tests('server', 'Lily')
        Router.perform_tests('server', 'Lily')
        Subnet.perform_tests('server', 'Lily')
        Port.perform_tests('server', 'Lily')
        # Trunk.perform_tests('server', 'Lily')
        Bgpvpn.perform_tests('server', 'Lily')
        Firewall.perform_tests('server', 'Lily')
        FirewallPolicy.perform_tests('server', 'Lily')
        FirewallRule.perform_tests('server', 'Lily')
        FloatingIP.perform_tests('server', 'Lily')
        Gateway.perform_tests('server', 'Lily')
        GatewayConnection.perform_tests('server', 'Lily')
        Loadbalancer.perform_tests('server', 'Lily')
        LoadbalancerHealthMonitor.perform_tests('server', 'Lily')
        LoadbalancerListener.perform_tests('server', 'Lily')
        LoadbalancerPool.perform_tests('server', 'Lily')
        MeteringLabel.perform_tests('server', 'Lily')
        MeteringLabelRule.perform_tests('server', 'Lily')
        QosPolicy.perform_tests('server', 'Lily')
        VpnService.perform_tests('server', 'Lily')
        SecurityGroupRule.perform_tests('server', 'Lily')
        # SecurityGroup.perform_tests('server', 'admin')
        SFCFlowClassifier.perform_tests('server', 'Lily')
        SFCPortChain.perform_tests('server', 'Lily')
        SFCPortPair.perform_tests('server', 'Lily')
        SFCPortPairGroup.perform_tests('server', 'Lily')


        logging.info('Test End')

    latency.log_to_xls(filename, 'Sloth_100_5', 10)  # filter means the first 10 results are just erased

    # new start: 3  4  6

    # latency.latency_data_transform(filename, 'Origin')


