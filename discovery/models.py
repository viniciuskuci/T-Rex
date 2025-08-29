from zeroconf import ServiceInfo
from dataclasses import dataclass
from enum import Enum

class DiscoveryEvent(Enum):
    ADDED = "add"
    REMOVED = "remove"
    UPDATED = "update"

@dataclass
class Service:
    info: ServiceInfo
    event: DiscoveryEvent