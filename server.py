import socket
import threading
import yahtzeeGame as yg

games = {}  # game_id: (game, [player1, player2])
next_game_id = 1
player_states = {}  # player: state

def handle_client(conn, addr, game_id):
    print(f'Connected by {addr}')
    game, players = games[game_id]
    player_index = players.index((conn, addr))  # Determine which player this client is
    player_states[player_index] = 'start'  # Initialize player state to 'start'
    roll_count = [0]  # Number of rolls this turn
    with conn:
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            print(f'Received from client{addr}: {data}')
            if data.startswith('ready'):    # Ignore the 'ready' message but print the identifier
                print(f'Received ready message from {data[5:]}')
                continue
            response = ""
            if game.current_player != player_index:
                print(f'Player {player_index} tried to play out of turn')  # Debug print
                response = "It's not your turn"
            else:
                if data == 'roll':
                    if player_states[player_index] == 'start' or (player_states[player_index] == 'keep' and roll_count[0] < 2):
                        roll_count[0] += 1
                        response = game.roll_dice()
                        player_states[player_index] = 'keep'
                    else:
                        print(f'Player {player_index} tried to roll when not allowed')  # Debug print
                        response = "You can't roll now"
                elif data.startswith('keep'):
                    if player_states[player_index] == 'keep' and roll_count[0] < 3:
                        _, *kept = data.split()
                        kept = list(map(int, kept))
                        response = game.roll_dice(keep=kept)
                        roll_count[0] += 1
                        if roll_count[0] == 3:
                            player_states[player_index] = 'score'
                    else:
                        print(f'Player {player_index} tried to keep when not allowed')  # Debug print
                        response = "You can't keep now"
                elif data.startswith('score'):
                    if player_states[player_index] == 'score':
                        _, category = data.split()
                        response = game.calculate_score(category)
                        player_states[player_index] = 'add'
                    else:
                        print(f'Player {player_index} tried to score when not allowed')  # Debug print
                        response = "You can't score now"
                elif data.startswith('add'):
                    if player_states[player_index] == 'add':
                        _, category = data.split()
                        response = game.add_score(category)
                        game.switch_player()  # Switch player after a valid command
                        player_states[player_index] = 'start'
                        roll_count[0] = 0  # Reset roll count
                    else:
                        print(f'Player {player_index} tried to add when not allowed')  # Debug print
                        response = "You can't add now"
                else:
                    print(f'Player {player_index} sent an unknown command: {data}')  # Debug print
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
                    if len(players) == 2:  # Start the game only when both players have connected
                        game.current_player = 0  # Set the first connected client as the current player
                        for player in players:
                            client_thread = threading.Thread(target=handle_client, args=(player[0], player[1], game_id))
                            client_thread.start()
                            print(f'Started thread for client at {addr}')  # Debug print
                    break
            else:
                game = yg.YahtzeeGame()
                games[next_game_id] = (game, [(conn, addr)])
                game_id = next_game_id
                next_game_id += 1

if __name__ == "__main__":
    start_server()