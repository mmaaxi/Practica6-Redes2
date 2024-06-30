import os
import socket
import threading

# Configuración del peer
PEER_HOST = 'localhost'
PEER_PORT = 5000  
DIRECTORY = 'files'

PEERS = [
    ('localhost', 5000),
    ('localhost', 5001),
    ('localhost', 5002),
    ('localhost', 5003)
]

def list_files():
    return os.listdir(DIRECTORY)

def handle_client(conn, addr):
    print(f"Conexión establecida desde {addr}")
    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break
            
            command, _, filename = data.partition(' ')
            if command == 'B':
                files = list_files()
                response = '\n'.join(files)
                conn.send(response.encode())
            elif command == 'D' and filename:
                file_path = os.path.join(DIRECTORY, filename)
                if os.path.exists(file_path):
                    with open(file_path, 'rb') as file:
                        conn.sendall(file.read())
                else:
                    conn.send(b'Archivo no encontrado')
            else:
                conn.send(b'Comando no reconocido')
        except Exception as e:
            print(f"Error: {e}")
            break

    conn.close()
    print(f"Conexión cerrada con {addr}")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((PEER_HOST, PEER_PORT))
    server.listen()
    print(f"Peer escuchando en {PEER_HOST}:{PEER_PORT}")

    while True:
        conn, addr = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()

def search_file(filename):
    # Búsqueda local
    local_files = list_files()
    if filename in local_files:
        print(f"Archivo '{filename}' encontrado localmente en '{DIRECTORY}'")
        return

    # Búsqueda en otros peers
    for peer in PEERS:
        if peer[1] == PEER_PORT:
            continue
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(peer)
                s.send(f'B {filename}'.encode())

                data = s.recv(1024).decode()
                files = data.splitlines()

                if filename in files:
                    print(f"Archivo '{filename}' encontrado en el peer {peer}")
                    return
        except Exception as e:
            print(f"Error conectando a {peer}: {e}")
    print(f"Archivo '{filename}' no encontrado en ningún peer")

def download_file(filename):
    # Búsqueda en otros peers
    for peer in PEERS:
        if peer[1] == PEER_PORT:
            continue
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(peer)
                s.send(f'B {filename}'.encode())

                data = s.recv(1024).decode()
                files = data.splitlines()

                if filename in files:
                    s.send(f'D {filename}'.encode())
                    new_filename = f"descargado_{filename}"
                    with open(os.path.join(DIRECTORY, new_filename), 'wb') as file:
                        file.write(s.recv(1024 * 1024))
                    print(f"Archivo '{filename}' descargado desde el peer {peer} como '{new_filename}'")
                    return
        except Exception as e:
            print(f"Error conectando a {peer}: {e}")
    print(f"Archivo '{filename}' no encontrado en ningún peer")

if __name__ == "__main__":
    threading.Thread(target=start_server).start()

    while True:
        command = input("Ingrese comando (B/D nombrearchivo): ")
        if command.startswith('B'):
            _, filename = command.split(' ', 1)
            search_file(filename)
        elif command.startswith('D'):
            _, filename = command.split(' ', 1)
            download_file(filename)
        else:
            print("Comando no válido")
