import socket


HOST = '0.0.0.0'
PORT = 12345

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    server.settimeout(1.0) 

    print(f"[SERVER] Nasłuchuję na {HOST}:{PORT}")

    while True:
        try: 
            connection, _ = server.accept()
        except socket.timeout:
            pass
        except Exception as e:
            print("Błąd połączenie klienta: ", e)

start_server()