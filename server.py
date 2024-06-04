import socket
import threading
import yahtzeeGame as yg

games = {}  # game_id: (game, [player1, player2])
next_game_id = 1

def handle_client(conn, addr, game_id):
    print(f'Connected by {addr}')
    game, players = games[game_id]
    player_index = players.index((conn, addr))  # Determine which player this client is
    with conn:
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            print(f'Received from client: {data}')
            response = ""
            if game.current_player != player_index:
                response = "It's not your turn"
            else:
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
                game.switch_player()  # Switch player after each command
            conn.sendall(str(response).encode())

def start_server(host='localhost', port=65432):
    global next_game_id
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f'Server started at {host}:{port}')
        while True:
            conn, addr = s.accept()
            for game_id, (game, players) in games.items():
                if len(players) < 2:
                    players.append((conn, addr))
                    break
            else:
                game = yg.YahtzeeGame()
                games[next_game_id] = (game, [(conn, addr)])
                game_id = next_game_id
                next_game_id += 1
            client_thread = threading.Thread(target=handle_client, args=(conn, addr, game_id))
            client_thread.start()

if __name__ == "__main__":
    start_server()