import socket
import threading
import dns.resolver   # install with: pip install dnspython

HOST = "127.0.0.1"
PORT = 5050

# --- Utility: Check if host/port is open ---
def check_host_port(host, port, timeout=3):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return f"[OK] {host}:{port} is OPEN"
    except Exception:
        return f"[FAIL] {host}:{port} is CLOSED"

# --- Utility: DNS lookup ---
def dns_lookup(domain, record_type="A"):
    try:
        answers = dns.resolver.resolve(domain, record_type)
        return f"{record_type} records for {domain}: {[str(r) for r in answers]}"
    except Exception as e:
        return f"[ERROR] {e}"

# --- Handle client connections ---
def handle_client(conn, addr):
    print(f"[CONNECTED] {addr}")
    conn.sendall(b"Welcome to MCP Server!\nCommands: CHECK <host> <port>, DNS <domain> <type>, EXIT\n")

    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            message = data.decode().strip()
            print(f"[COMMAND from {addr}] {message}")

            if message.upper() == "EXIT":
                conn.sendall(b"Goodbye!\n")
                break

            parts = message.split()
            if len(parts) == 3 and parts[0].upper() == "CHECK":
                response = check_host_port(parts[1], int(parts[2]))
            elif len(parts) == 3 and parts[0].upper() == "DNS":
                response = dns_lookup(parts[1], parts[2].upper())
            else:
                response = "❓ Unknown command. Use CHECK <host> <port> or DNS <domain> <type>"

            conn.sendall((response + "\n").encode())

        except Exception as e:
            print(f"[ERROR {addr}] {e}")
            break

    conn.close()
    print(f"[DISCONNECTED] {addr}")

# --- Start server ---
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()

    print(f"[STARTED] MCP Server running on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    start_server()
