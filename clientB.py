import socket
import time

def start_client(host='localhost', port=65433):
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))
                print('Client B is ready')
                s.sendall(b'readyB')
                print(f'Connected to server at {host}:{port}')
                while True:
                    message = input('Enter command (roll, keep <indices>, score <category>, add <category>, reset, exit): ')
                    if message.lower() == 'exit':
                        break
                    s.sendall(message.encode())
                    data = s.recv(1024)
                    print(f'Received from server: {data.decode()}')
                break  # If the connection is successful, break the loop
        except ConnectionRefusedError:
            print('Connection refused, retrying in 1 second...')
            time.sleep(1)  # Wait for 1 second before retrying

if __name__ == "__main__":
    start_client()