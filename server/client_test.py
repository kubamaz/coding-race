import socket
import time
SERVER_IP = '127.0.0.1'
PORT = 12345

isConnected = False

try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_IP, PORT))
    isConnected = True
except Exception as e:
    print(f"Error connecting to server: {e}")

while isConnected:
    try:
        client.sendall(b"TEST")
    except Exception as e:
        print(f"Error sending data: {e}")
        isConnected = False
        break
    print("Połączono.")
    time.sleep(1)
    pass