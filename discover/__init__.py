"""
Discover package for handling discovery of available services on the network.
Discovery protocol: mDNS (Multicast DNS)
Service specifications: 
    _dinasore._tcp.local.
Possible service types:
    - FBT_random
This package launches a process that listens for mDNS announcements and stores new services in a local database.

"""