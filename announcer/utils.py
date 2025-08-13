import socket

def get_self_ip():
    """
    Get the local IP address of the current machine.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
        
    except OSError as e:
        print(f"Error getting local IP address: {e}")
        return None

def get_self_hostname() -> str:
    """
    Get the hostname of the current machine without the '.local' suffix.
    """
    hostname = socket.gethostname()
    if hostname.endswith('.local'):
        hostname = hostname[:-6]
    return hostname
 