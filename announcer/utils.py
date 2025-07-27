import socket
import uuid

def get_self_ip():
    """
    Get the local IP address of this machine.
    
    Returns:
        str: Local IP address.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
        
    except OSError as e:
        print(f"Error getting local IP address: {e}")
        return None

def get_self_hostname():
    """
    Get a unique hostname for this machine.
    
    Returns:
        str: Hostname with identifier.
    """
    hostname = socket.gethostname()
    if hostname.endswith('.local'):
        hostname = hostname[:-6]
    return hostname
 