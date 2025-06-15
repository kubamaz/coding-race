import socket
import threading
import json
import time
HOST = '0.0.0.0'
PORT = 12345

Running = True
player_list = []
queue = []
def addr_to_str(addr):
    return f"{addr[0]}:{addr[1]}"

def handle_client(connection):
    print(f"[+] Nowy gracz: {connection.getpeername()}")

    player_list.append(connection)
    looking_for_opponent = True
    while looking_for_opponent:
        try:
            data = connection.recv(1024).decode()
            if not data:
                print(f"[!] Gracz {connection.getpeername()} rozłączył się.")
                connection.close()
                player_list.remove(connection)
                if connection in queue:
                    queue.remove(connection)
                return
            
            while '\n' in data:
                message, data = data.split('\n', 1)
                message = message.strip()

                msg = json.loads(message)
                if msg.get("type") == "join" and not connection in queue:
                    print(f"[+] Gracz {connection.getpeername()} dołączył do gry.")
                    queue.append(connection)
                elif msg.get("type") == "leave":
                    queue.remove(connection)
                    print(f"[!] Gracz {connection.getpeername()} opuścił kolejkę.")
                elif msg.get("type") == "match":
                    return
        except Exception as e:
            print(f"Błąd odbierania danych od gracza {connection.getpeername()}: {e}")
            connection.close()
            player_list.remove(connection)
            return

def handle_player(player, opponent):
    while Running:
        try:
            data = player.recv(2048).decode()
            if not data:
                print(f"[!] Gracz {player.getpeername()} rozłączył się.")
                player.close()
                # Powiadom przeciwnika o rozłączeniu
                opponent.sendall((json.dumps({
                    "type": "opponent_disconnected",
                    "message": "Twój przeciwnik rozłączył się."
                }) + '\n').encode())
                break

            while '\n' in data:
                dane, data = data.split('\n', 1)
                dane = dane.strip()
                if not dane:
                    continue

                msg = json.loads(dane)

                if msg.get("type") == "winner":
                    print(f"Otrzymano komunikat o zwycięstwie: {msg.get('message')}")
                    # Powiadom przeciwnika, że przegrał
                    opponent.sendall((json.dumps({
                        "type": "looser",
                        "message": "Twój przeciwnik wygrał!",
                    }) + '\n').encode())
                    # Zamknij oba połączenia
                    player.close()
                    opponent.close()
                    if player in player_list:
                        player_list.remove(player)
                    if opponent in player_list:
                        player_list.remove(opponent)
                    return

                opponent.sendall((json.dumps(msg) + '\n').encode())

        except Exception as e:
            print(f"Błąd odbierania danych od gracza {player.getpeername()}: {e}")
            player.close()
            try:
                if player in player_list:
                    player_list.remove(player)
                
                opponent.sendall((json.dumps({
                    "type": "opponent_disconnected",
                    "message": "Twój przeciwnik rozłączył się."
                }) + '\n').encode())
                opponent.close()
                if opponent in player_list:
                    player_list.remove(opponent)
            except:
                pass
            break
def handle_game(player1 , player2):
    t1 = threading.Thread(target=handle_player, args=(player1, player2))
    t2 = threading.Thread(target=handle_player, args=(player2, player1))

    t1.start()
    t2.start()

    t1.join()
    t2.join()
                

def queue_system():
     while Running:
        time.sleep(5)
        if (len(queue) >= 2):
            player1 = queue.pop(0)
            player2 = queue.pop(0)
            try:
                player1.sendall((json.dumps({
                    "type": "match",
                    "message": "Znalazłeś przeciwnika!",
                    "player_id": player1.getpeername(),
                    "car": 1,
                }) + '\n').encode())
                player2.sendall((json.dumps({
                    "type": "match",
                    "message": "Znalazłeś przeciwnika!",
                    "player_id": player2.getpeername(),
                    "car": 2,
                }) + '\n').encode())

                print(f"[+] Rozpoczynam grę między {player1.getpeername()} a {player2.getpeername()}")
                time.sleep(3)  # Daj czas na wysłanie wiadomości do graczy
                game_thread = threading.Thread(target=handle_game, args=(player1, player2), daemon=True)
                game_thread.start()
                
            except Exception as e:
                print(f"Błąd wysyłania danych do graczy: {e}")
                player1.close()
                player2.close()
                if player1 in player_list:
                    player_list.remove(player1)
                if player2 in player_list:
                    player_list.remove(player2)

def server_console():
    global Running
    while Running:
        cmd = input()
        if cmd == "exit":
            Running = False
            for player in player_list:
                player.sendall((json.dumps({
                    "type": "server_shutdown",
                    "message": "Serwer jest zamykany, do zobaczenia!"
                }) + '\n').encode())
                player.close()
                player_list.remove(player)
            print("[SERVER] Zamykanie serwera...")
            break
        elif cmd == "players":
            print("[SERVER] Lista graczy:")
            for player in player_list:
                print(f" - {player.getpeername()}")
        elif cmd == "queue":
            print("[SERVER] Gracze w kolejce:")
            for player in queue:
                print(f" - {player.getpeername()}")
        elif cmd == "help":
            print("[SERVER] Dostępne komendy:")
            print(" - exit: Zamyka serwer")
            print(" - players: Wyświetla listę graczy")
            print(" - queue: Wyświetla graczy w kolejce")
            print(" - help: Wyświetla tę pomoc")
        else:
            print("[SERVER] Nieznana komenda. Użyj 'help' aby zobaczyć dostępne komendy.")

def start_server():
    global Running
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    server.settimeout(1.0) 

    print(f"[SERVER] Nasłuchuję na {HOST}:{PORT}")

    console_thread = threading.Thread(target=server_console, daemon=True)
    console_thread.start()

    queue_system_thread = threading.Thread(target=queue_system, daemon=True)
    queue_system_thread.start()
    while Running:
        try: 
            connection, _ = server.accept()
            client_thread = threading.Thread(target=handle_client, args=(connection,), daemon=True)
            client_thread.start()
        except socket.timeout:
            pass
        except Exception as e:
            print("Błąd połączenie klienta: ", e)
    server.close()
    print("[SERVER] Serwer został zamknięty.")

start_server()