import socket
# import time
import json
import threading
# SERVER_IP = '127.0.0.1'
# PORT = 12345

# PlayerID = 1

# isConnected = False
# isPlaying = False

# def addr_to_str(addr):
#     return f"{addr[0]}:{addr[1]}"

# try:
#     client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     client.connect((SERVER_IP, PORT))
#     isConnected = True
# except Exception as e:
#     print(f"Error connecting to server: {e}")

# def send_data():
#     try:
#         msg = {
#             "type": "update_position",
#             "x": 100,
#             "y": 200,
#             "angle": 90,
#             "speed": 5,
#             "boost": True,
#             "lap": 1,
#             "correct_answer": 3,
#             "questions": 3,
#             "is_answering": False,
#             "player_id": addr_to_str(PlayerID),
#         }
#         client.sendall((json.dumps(msg) + '\n').encode())
#     except Exception as e:
#         print(f"Error sending data: {e}")

# def recive_data():
#     global isConnected
#     global PlayerID
#     global isPlaying
#     while isConnected:
#         try:
#             data = client.recv(1024).decode()
#             while '\n' in data:
#                 dane, data = data.split('\n', 1)
#                 dane = dane.strip()
#                 if dane:
#                     msg = json.loads(dane)
#                     if msg.get("type") == "server_shutdown":
#                         print(f"Otrzymano komunikat o zamknięciu serwera: {msg.get('message')}")
#                         isConnected = False
#                         break
#                     elif msg.get("type") == "update_position":
#                         print(f"Otrzymano aktualizację pozycji: {msg}")
#                     elif msg.get("type") == "queue":
#                         print(f"Otrzymano komunikat o kolejce: {msg.get('message')}")
#                         PlayerID = msg.get("player_id", PlayerID)
#                     elif msg.get("type") == "match":
#                         isPlaying = True
#                         print(f"Otrzymano komunikat o rozpoczęciu meczu: {msg.get('message')}")
#                     elif msg.get("type") == "opponent_disconnected":
#                         print(f"Otrzymano komunikat o rozłączeniu przeciwnika: {msg.get('message')}")
#                         isPlaying = False
#                         isConnected = False
#                     elif msg.get("type") == "winner":
#                         print(f"Otrzymano komunikat o zwycięstwie: {msg.get('message')}")
#                         isPlaying = False
#                         isConnected = False
#                         client.close()
#                     elif msg.get("type") == "looser":
#                         print(f"Otrzymano komunikat o przegranej: {msg.get('message')}")
#                         isPlaying = False
#                         isConnected = False
#                         client.close()
#                     else:
#                         print(f"Otrzymano nieznany komunikat: {msg}")
#         except Exception as e:
#             print(f"Błąd odbierania danych: {e}")
#             isConnected = False
#             break

# if isConnected:
#     recv_thread = threading.Thread(target=recive_data, daemon=True)
#     recv_thread.start()
#     while isConnected:
#         if isPlaying:
#             send_data()
#         time.sleep(0.1) # Wysyłaj dane co 0.1 sekundy



class Networking:
    def __init__(self, server_ip='127.0.0.1', port=12345):
        self.server_ip = server_ip
        self.port = port
        self.client = None
        self.is_connected = False
        self.is_playing = False
        self.player_id = 1

        self.couldnt_connect = False
        self.looking_for_match = False
        self.found_match = False
        self.car = None
        self.opponent_disconnected = False
        self.server_shutdown = False
        self.recv_thread = None
        self.current_oponent_data = None
    
    def addr_to_str(self, addr):
        return f"{addr[0]}:{addr[1]}" if isinstance(addr, tuple) else str(addr)

    def connect(self):
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((self.server_ip, self.port))
            self.is_connected = True
        except Exception as e:
            self.couldnt_connect = True
    
    def send_data(self, data=None):
        if not self.is_connected:
            return
        try:
            msg = data 
            #  {
            #     "type": "update_position",
            #     "x": 100,
            #     "y": 200,
            #     "angle": 90,
            #     "speed": 5,
            #     "boost": True,
            #     "lap": 1,
            #     "correct_answer": 3,
            #     "questions": 3,
            #     "is_answering": False,
            #     "player_id": self.addr_to_str(self.player_id),
            # }
            self.client.sendall((json.dumps(msg) + '\n').encode())
        except Exception as e:
            pass
    
    def receive_data(self):
        while self.is_connected:
            try:
                data = self.client.recv(1024).decode()
                while '\n' in data:
                    line, data = data.split('\n', 1)
                    line = line.strip()
                    if line:
                        msg = json.loads(line)
                        self.handle_message(msg)
            except Exception as e:
                self.is_connected = False
                break
    
    def handle_message(self, msg):
        msg_type = msg.get("type")

        if msg_type == "server_shutdown":
            self.server_shutdown = True
            self.is_connected = False

        elif msg_type == "update_position":
            self.current_oponent_data = {
                "x": msg.get("x"),
                "y": msg.get("y"),
                "angle": msg.get("angle"),
                "speed": msg.get("speed"),
                "boost": msg.get("boost"),
                "lap": msg.get("lap"),
                "correct_answer": msg.get("correct_answer"),
                "questions": msg.get("questions"),
                "is_answering": msg.get("is_answering"),
                "player_id": msg.get("player_id")
            }

        elif msg_type == "match":
            print("Match found")
            self.is_playing = True
            self.found_match = True
            self.looking_for_match = False
            self.car = msg.get("car", None)
            print(self.car)
            self.player_id = msg.get("player_id", self.player_id)
            self.send_data({
                "type": "match"
            })
            

        elif msg_type == "opponent_disconnected":
            self.opponent_disconnected = True
            self.is_playing = False
            self.is_connected = False

        elif msg_type == "winner":
            self.is_playing = False
            self.is_connected = False
            self.client.close()

        elif msg_type == "looser":
            self.is_playing = False
            self.is_connected = False
            self.client.close()
        
    
    def start_receiving(self):
        if self.is_connected:
            self.recv_thread = threading.Thread(target=self.receive_data, daemon=True)
            self.recv_thread.start()
