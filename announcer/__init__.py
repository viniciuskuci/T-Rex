"""
Announcer package for handling available services on the network.
Discovery protocol: mDNS (Multicast DNS)
Service specifications: 
    _dinasore._tcp.local.
Possible service types:
    - FBT_random
This package launches services in a local network via mDNS.

"""

from .announcer import Announcer

__all__ = ['Announcer']