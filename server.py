import socket
import sys
import threading
import yahtzeeGame as yg

games = {}  # game_id: (game, [player1, player2])
next_game_id = 1
player_states = {}  # player: state

def handle_client(conn, addr, game_id):
    print(f'Connected by {addr}')
    game, players = games[game_id]
    player_index = players.index((conn, addr))  # Determine which player this client is
    player_states[player_index] = 'roll'  # Initialize player state to 'roll'
    with conn:
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            print(f'Received from client: {data}')
            response = ""
            if game.current_player != player_index:
                print(f'Player {player_index} is trying to play out of turn')
                print(f'Current player is {game.current_player}')
                print(f'Player states: {player_states}')
                print(f'Game: {game}')
                print(f'Players: {players}')
                print(f'Game ID: {game_id}')
                print(f'Games: {games}')
                print(f'Next game ID: {next_game_id}')
                response = "It's not your turn"
            else:
                if data == 'roll':
                    if player_states[player_index] == 'roll':
                        response = game.roll_dice()
                        player_states[player_index] = 'keep'
                    else:
                        response = "You can't roll now"
                elif data.startswith('keep'):
                    if player_states[player_index] == 'keep':
                        _, *kept = data.split()
                        kept = list(map(int, kept))
                        response = game.roll_dice(keep=kept)
                        player_states[player_index] = 'score'
                    else:
                        response = "You can't keep now"
                elif data.startswith('score'):
                    if player_states[player_index] == 'score':
                        _, category = data.split()
                        response = game.calculate_score(category)
                        player_states[player_index] = 'add'
                    else:
                        response = "You can't score now"
                elif data.startswith('add'):
                    if player_states[player_index] == 'add':
                        _, category = data.split()
                        response = game.add_score(category)
                        game.switch_player()  # Switch player after a valid command
                        player_states[player_index] = 'roll'
                    else:
                        response = "You can't add now"
                else:
                    response = "Unknown command"
            conn.sendall(str(response).encode())
def start_server(host='localhost', port=65433):
    global next_game_id
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f'Server started at {host}:{port}')
        while True:
            conn, addr = s.accept()
            conn.sendall(b'ready')
            for game_id, (game, players) in games.items():
                if len(players) < 2:
                    players.append((conn, addr))
                    break
            else:
                game = yg.YahtzeeGame()
                game.current_player = 0 # Set the first connected client as the current player
                games[next_game_id] = (game, [(conn, addr)])
                game_id = next_game_id
                next_game_id += 1
            client_thread = threading.Thread(target=handle_client, args=(conn, addr, game_id))
            client_thread.start()

if __name__ == "__main__":
    start_server()