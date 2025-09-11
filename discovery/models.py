from zeroconf import ServiceInfo
from dataclasses import dataclass
from enum import Enum
import socket


def get_self_ip():
    try:
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        return ip
    except Exception as e:
        print(f"Error getting local IP: {e}")
        return None


def get_self_hostname() -> str:

    hostname = socket.gethostname()
    if hostname.endswith(".local"):
        hostname = hostname[:-6]
    return hostname


class Constants(Enum):
    DISCOVERY_TIMEOUT = 5
    DINASORE_SERVICE_TYPE = "_dinasore._tcp.local."
    DINASORE_PORT = 2901
    ROLE_GATEWAY = "gateway"
    ROLE_WORKER = "worker"


class DiscoveryEvent(Enum):
    ADDED = "add"
    REMOVED = "remove"
    UPDATED = "update"


class DinasoreService:

    @staticmethod
    def worker() -> ServiceInfo:
        ip = get_self_ip()
        name = f"{get_self_hostname()}.{Constants.DINASORE_SERVICE_TYPE.value}"

        return ServiceInfo(
            type_=Constants.DINASORE_SERVICE_TYPE.value,
            name=name,
            addresses=[socket.inet_aton(ip)],
            port=Constants.DINASORE_PORT.value,
            properties={"role": Constants.ROLE_WORKER.value},
        )

    @staticmethod
    def gateway() -> ServiceInfo:
        ip = get_self_ip()
        name = f"{get_self_hostname()}.{Constants.DINASORE_SERVICE_TYPE.value}"

        return ServiceInfo(
            type_=Constants.DINASORE_SERVICE_TYPE.value,
            name=name,
            addresses=[socket.inet_aton(ip)],
            port=Constants.DINASORE_PORT.value,
            properties={"role": Constants.ROLE_GATEWAY.value},
        )
