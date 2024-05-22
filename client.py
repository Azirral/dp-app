import socket

def start_client(host='localhost', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        print(f'Connected to server at {host}:{port}')
        while True:
            message = input('Enter command (roll, keep <indices>, score <category>, add <category>, reset, exit): ')
            if message.lower() == 'exit':
                break
            s.sendall(message.encode())
            data = s.recv(1024)
            print(f'Received from server: {data.decode()}')

if __name__ == "__main__":
    start_client()