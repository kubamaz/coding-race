import socket
import threading
import json
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
    #TODO connection handle, queue system etc 

def server_console():
    global Running
    while Running:
        cmd = input()
        if cmd == "exit":
            Running = False
            for player in player_list:
                player.close()
                player_list.remove(player)
            print("[SERVER] Zamykanie serwera...")
            break
        elif cmd == "players":
            print("[SERVER] Lista graczy:")
            for player in player_list:
                print(f" - {player.getpeername()}")
        elif cmd == "help":
            print("[SERVER] Dostępne komendy:")
            print(" - exit: Zamyka serwer")
            print(" - players: Wyświetla listę graczy")
            print(" - help: Wyświetla tę pomoc")

def start_server():
    global Running
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    server.settimeout(1.0) 

    print(f"[SERVER] Nasłuchuję na {HOST}:{PORT}")

    console_thread = threading.Thread(target=server_console, daemon=True)
    console_thread.start()
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