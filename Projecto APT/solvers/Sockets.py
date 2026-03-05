import json
import socket

def listen_socket():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 65535))
    server_socket.listen(1)
    print("Server is listening on port 65535")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")

        data = client_socket.recv(1024)
        if not data:
            client_socket.close()
            break

        json_data = json.loads(data.decode('utf-8'))

        return json_data
    
def send_to_cli(result_data):
    cli_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cli_socket.connect(('localhost', 62000))
    cli_socket.sendall(json.dumps(result_data).encode('utf-8'))
    print("enviado")
    cli_socket.close()

if __name__ == "__main__":
    listen_socket()
