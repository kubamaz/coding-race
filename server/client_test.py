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
                if msg.get("type") != "ping":
                    print(f"Otrzymano dane: {msg}")
        except Exception as e:
            print(f"Błąd odbierania danych: {e}")
            isConnected = False
            break

if isConnected:
    recv_thread = threading.Thread(target=recive_data, daemon=True)
    recv_thread.start()

while isConnected:
    try:
        client.sendall(b"TEST")
    except Exception as e:
        print(f"Nie udało się wysłać danych: {e}")
        isConnected = False
        break
    time.sleep(1)
    pass