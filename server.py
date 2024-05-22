import socket
import threading
import yahtzeeGame as yg


def handle_client(conn, addr, game):
    print(f'Connected by {addr}')
    with conn:
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            print(f'Received from client: {data}')
            response = ""
            if data == 'roll':
                response = game.roll_dice()
            elif data.startswith('keep'):
                _, *kept = data.split()
                kept = list(map(int, kept))
                response = game.roll_dice(keep=kept)
            elif data == 'reset':
                game.reset()
                response = "Game reset"
            elif data.startswith('score'):
                _, category = data.split()
                response = game.calculate_score(category)
            elif data.startswith('add'):
                _, category = data.split()
                response = game.add_score(category)
            else:
                response = "Unknown command"
            conn.sendall(str(response).encode())

def start_server(host='localhost', port=65432):
    game = yg.YahtzeeGame()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f'Server started at {host}:{port}')
        while True:
            conn, addr = s.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr, game))
            client_thread.start()

if __name__ == "__main__":
    start_server()
