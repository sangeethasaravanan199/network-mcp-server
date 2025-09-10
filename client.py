import socket

HOST = "127.0.0.1"
PORT = 5050

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print(s.recv(1024).decode())  # welcome msg

    while True:
        cmd = input(">> ")
        s.sendall(cmd.encode())
        if cmd.upper() == "EXIT":
            break
        print(s.recv(4096).decode())
