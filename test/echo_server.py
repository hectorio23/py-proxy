# /usr/bin/python3
import socket

ADDRESS = "127.0.0.1"
PORT = 3747

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ADDRESS, PORT))

server.listen(5)

print(f"Serving on ({ ADDRESS }, { PORT })")

while True:
    client_socket, client_address = server.accept()
    print(f"Device {client_address} connected")
    data = client_socket.recv(1024)
    print(f"Data received from {client_address}: {data.decode('UTF-8')}")
    client_socket.close()