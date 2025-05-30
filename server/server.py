import socket
import threading
HOST = '0.0.0.0'
PORT = 12345

def handle_client(connection):
    print(f"[+] Nowy gracz: {connection.getpeername()}")
    #TODO connection handle, queue system etc 


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    server.settimeout(1.0) 

    print(f"[SERVER] Nasłuchuję na {HOST}:{PORT}")

    while True:
        try: 
            connection, _ = server.accept()
            client_thread = threading.Thread(target=handle_client, args=(connection,), daemon=True)
            client_thread.start()
        except socket.timeout:
            pass
        except Exception as e:
            print("Błąd połączenie klienta: ", e)

start_server()