import socket
import threading
import json
import time
HOST = '0.0.0.0'
PORT = 12345

Running = True
player_list = []
queue = []

def handle_client(connection):
    print(f"[+] Nowy gracz: {connection.getpeername()}")

    player_list.append(connection)

    try:
        connection.sendall(json.dumps({
            "type": "queue",
            "message": "Czekasz na przeciwnika..."
        }).encode())
        queue.append(connection)
    except Exception as e:
        print(f"Błąd wysyłania danych do gracza {connection.getpeername()}: {e}")
        connection.close()
        player_list.remove(connection)
        return
    
    while Running:
        time.sleep(5)
        try:
            connection.sendall(json.dumps({
                    "type": "ping",
                    "message": "pong!"
                }).encode())
        except Exception as e:
            print(f"Błąd wysyłania danych do gracza {connection.getpeername()}: {e}")
            connection.close()
            player_list.remove(connection)
            if connection in queue:
                queue.remove(connection)
            return
   

def queue_system():
     while Running:
        time.sleep(5)
        if (len(queue) >= 2):
            player1 = queue.pop(0)
            player2 = queue.pop(0)
            try:
                player1.sendall(json.dumps({
                    "type": "match",
                    "message": "Znalazłeś przeciwnika!"
                }).encode())
                player2.sendall(json.dumps({
                    "type": "match",
                    "message": "Znalazłeś przeciwnika!"
                }).encode())
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
                player.sendall(json.dumps({
                    "type": "server_shutdown",
                    "message": "Serwer jest zamykany, do zobaczenia!"
                }).encode())
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