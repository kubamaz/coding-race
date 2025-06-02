import socket

SERVER_IP = '127.0.0.1'
PORT = 12345

try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_IP, PORT))
except Exception as e:
    print(f"Error connecting to server: {e}")

while True:
    pass