import subprocess
import socket
import time

def wait_for_ready(host='localhost', port=65433):
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))
                data = s.recv(1024)
                print(f'Received: {data.decode()}')
                break  # If the connection is successful, break the loop
        except ConnectionRefusedError:
            print('Connection refused, retrying in 1 second...')
            time.sleep(1)  # Wait for 1 second before retrying

# Start the server
subprocess.Popen(["python", "server.py"], creationflags=subprocess.CREATE_NEW_CONSOLE)
wait_for_ready(port=65433)  # Wait for the server to be ready

# Start the first client
subprocess.Popen(["python", "clientA.py"], creationflags=subprocess.CREATE_NEW_CONSOLE)
wait_for_ready(port=65433)  # Wait for the first client to be ready

# Start the second client
subprocess.Popen(["python", "clientB.py"], creationflags=subprocess.CREATE_NEW_CONSOLE)
wait_for_ready(port=65433)  # Wait for the second client to be ready