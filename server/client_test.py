import socket
import time
import json
import threading
SERVER_IP = '127.0.0.1'
PORT = 12345

PlayerID = 1  # Example player ID, can be set dynamically

isConnected = False
isPlaying = False

def addr_to_str(addr):
    return f"{addr[0]}:{addr[1]}"

try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_IP, PORT))
    isConnected = True
except Exception as e:
    print(f"Error connecting to server: {e}")

def send_data():
    try:
        msg = {
            "type": "update_position",
            "x": 100,
            "y": 200,
            "angle": 90,
            "speed": 5,
            "boost": True,
            "lap": 1,
            "correct_answer": 3,
            "questions": 3,
            "is_answering": False,
            "player_id": addr_to_str(PlayerID),
        }
        client.sendall((json.dumps(msg) + '\n').encode())
    except Exception as e:
        print(f"Error sending data: {e}")

def recive_data():
    global isConnected
    global PlayerID
    global isPlaying
    while isConnected:
        try:
            data = client.recv(1024).decode()
            while '\n' in data:
                dane, data = data.split('\n', 1)
                dane = dane.strip()
                if dane:
                    msg = json.loads(dane)
                    if msg.get("type") == "ping":
                        pass
                    elif msg.get("type") == "server_shutdown":
                        print(f"Otrzymano komunikat o zamknięciu serwera: {msg.get('message')}")
                        isConnected = False
                        break
                    elif msg.get("type") == "update_position":
                        print(f"Otrzymano aktualizację pozycji: {msg}")
                    elif msg.get("type") == "queue":
                        print(f"Otrzymano komunikat o kolejce: {msg.get('message')}")
                        PlayerID = msg.get("player_id", PlayerID)
                    elif msg.get("type") == "match":
                        isPlaying = True
                        print(f"Otrzymano komunikat o rozpoczęciu meczu: {msg.get('message')}")
                    elif msg.get("type") == "opponent_disconnected":
                        print(f"Otrzymano komunikat o rozłączeniu przeciwnika: {msg.get('message')}")
                        isPlaying = False
                        isConnected = False
                    elif msg.get("type") == "winner":
                        print(f"Otrzymano komunikat o zwycięstwie: {msg.get('message')}")
                        isPlaying = False
                        isConnected = False
                        client.close()
                    elif msg.get("type") == "looser":
                        print(f"Otrzymano komunikat o przegranej: {msg.get('message')}")
                        isPlaying = False
                        isConnected = False
                        client.close()
                    else:
                        print(f"Otrzymano wiadomość: {msg}")
        except Exception as e:
            print(f"Błąd odbierania danych: {e}")
            isConnected = False
            break

if isConnected:
    recv_thread = threading.Thread(target=recive_data, daemon=True)
    recv_thread.start()
    while isConnected:
        if isPlaying:
            send_data()
        time.sleep(0.1) # Wysyłaj dane co 0.1 sekundy
