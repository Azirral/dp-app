import socket
import sys


def start_client(host='localhost', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        print(f'Connected to server at {host}:{port}')
        print("available categories:\n"
              " ones: None\n twos: None\n threes: None\n fours: None\n fives: None\n sixes: None\n"
              " three_of_a_kind: None\n four_of_a_kind: None\n full_house: None\n small_straight: None\n"
              " large_straight: None\n yahtzee: None\n chance: None\n")
        while True:
            message = input('Enter command (roll, keep <indices>, score <category>, add <category>, reset, exit): ')
            if message.lower() == 'exit':
                break
            s.sendall(message.encode())
            data = s.recv(1024)
            print(f'Received from server: {data.decode()}')

if __name__ == "__main__":
    print(f"You are player {sys.argv[1]}")
    start_client()