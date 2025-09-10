import socket

def check_port(host, port):
    try:
        port = int(port)
        with socket.create_connection((host, port), timeout=2):
            return f"Port {port} on {host} is OPEN"
    except (socket.timeout, ConnectionRefusedError, OSError):
        return f"Port {port} on {host} is CLOSED or not responding"
