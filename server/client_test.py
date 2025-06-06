import socket
import time
import json
import threading
SERVER_IP = '127.0.0.1'
PORT = 12345

isConnected = False

try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_IP, PORT))
    isConnected = True
except Exception as e:
    print(f"Error connecting to server: {e}")


def recive_data():
    global isConnected
    while isConnected:
        try:
            data = client.recv(1024)
            if data:
                msg = json.loads(data)
                if msg.get("type") == "ping":
                    pass
                elif msg.get("type") == "server_shutdown":
                    print(f"Otrzymano komunikat o zamknięciu serwera: {msg.get('message')}")
                    isConnected = False
                    break
                else:
                    print(f"Otrzymano wiadomość: {msg}")
        except Exception as e:
            print(f"Błąd odbierania danych: {e}")
            isConnected = False
            break

if isConnected:
    recv_thread = threading.Thread(target=recive_data)
    recv_thread.start()