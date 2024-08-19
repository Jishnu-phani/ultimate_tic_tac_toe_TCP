import socket
import threading
import ssl


def print_board(board):
    
    for i in range(9):
        if i % 3 == 0:
            print("-------------------------")
            
        for j in range(9):
            
            if j % 3 == 0:
                print("|", end=" ")
                
            print(board[i][j], end=" ")
            
        print("|")
        
    print("-------------------------")


def valid_move(board, move, sub_game):
    x, y = move
    return sub_game[0] <= x < sub_game[0] + 3 and sub_game[1] <= y < sub_game[1] + 3 and board[x][y] == "."      
        

def check_board(board, x, y):
    
    for i in range(3):
        
        if board[x+i][y] == board[x+i][y+1] == board[x+i][y+2] != ".":
            return True
        
        if board[x][y+i] == board[x+1][y+i] == board[x+2][y+i] != ".":
            return True
        
    if board[x][y] == board[x+1][y+1] == board[x+2][y+2] != ".":
        return True
    
    if board[x][y+2] == board[x+1][y+1] == board[x+2][y] != ".":
        return True
    
    return False


def print_outer_board(outer_board):
    
    for row in range(3):
        print(" | ".join(outer_board[row]))
        
        if row!=2:
            print("----------")
    


clients = []
def host_game(host,port):
    global clients
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((host,port))
    server.listen(2)

    
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile='C:/Users/jishn/OneDrive/Desktop/sem 4/CN/mini-project/Ultimate-tic-tac-toe-final/certificate.pem', keyfile='C:/Users/jishn/OneDrive/Desktop/sem 4/CN/mini-project/Ultimate_tic-tac-toe/key.pem')
    server = context.wrap_socket(server, server_side=True)

    
    while True:
        client, addr = server.accept()
        clients.append(client)

        if len(clients) == 1:  # If this is the first client in the list
            threading.Thread(target=process_clients).start()

    server.close()
    
    
def process_clients():
    global clients
    
    while len(clients) > 0:
        handle_connection(clients[0])
        clients.pop(0)

    
def handle_connection(client):
    board = [["." for _ in range(9)] for _ in range(9)]
    outer_board = [["." for _ in range(3)] for _ in range(3)]
    current_player = "X"
    sub_games = [(i, j) for i in range(0, 9, 3) for j in range(0, 9, 3)]

    sub_game = sub_games[0]  # Start with the first sub-game
    while True:
        if current_player == "X":
            print("\n\n---------------------------------------------------------------------------------------------------\n\n")
            
            if check_board(outer_board, 0, 0):              # check if previous player has won
                current_player1 = ""
                
                if current_player == "X":
                    current_player1 = "O"
                else:
                    current_player1 = "X"
                    
                print(f"Player {current_player1} wins the game!\n")
                print_outer_board(outer_board)
                print("\n")
                break
            
            print_board(board)
            print(f"Player {current_player}'s turn")

            while True:
                print(f"{current_player} to play at sub game ({(sub_game[0] // 3)+1}, {(sub_game[1] // 3)+1})\n")
                
                try:
                    
                    x = input("Enter row: ")
                    print("\n")
                    
                    if x == "p":
                        print_outer_board(outer_board)
                        print("\n")
                        continue
                    
                    x = int(x)
                    y = int(input("Enter column: "))
                    print("\n")
                    x = x-1
                    y = y-1
                    
                    if valid_move(board, (x, y), sub_game):
                        a = str(x)
                        b = str(y)
                        client.send(a.encode('utf-8'))
                        client.send(b.encode('utf-8'))
                        break
                    
                except ValueError:
                    print("Invalid input, please enter a number.\n")
                print("Invalid move, try again.\n")

            board[x][y] = current_player

            if check_board(board, sub_game[0], sub_game[1]):
                
                if  outer_board[sub_game[0] // 3][sub_game[1] // 3] == ".":
                    outer_board[sub_game[0] // 3][sub_game[1] // 3] = current_player
                    print_board(board)
                    print(f"Player {current_player} wins sub-game at {(sub_game[0] // 3)+1}, {(sub_game[1] // 3)+1}!\n")
                    print_outer_board(outer_board)
                    
                    if check_board(outer_board, 0, 0):
                        print(f"Player {current_player} wins the game!\n")
                        break
                
            current_player = "O" if current_player == "X" else "X"  # Switch player after each move
            next_sub_game_row = (x%3)*3
            next_sub_game_col = (y%3)*3
            sub_game = (next_sub_game_row, next_sub_game_col)
            
            
            try:
                for q in range(9):
                    for w in range(9):
                        if board[q][w] == ".":
                            raise StopIteration
                print("Its a tie!")
                break
            except StopIteration:
                pass
        
        else:
            x = client.recv(1024)
            y = client.recv(1024)
            x = int(x.decode('utf-8'))
            y = int(y.decode('utf-8'))
            board[x][y] = current_player

            if check_board(board, sub_game[0], sub_game[1]):
                
                if outer_board[sub_game[0] // 3][sub_game[1] // 3] == ".":
                    outer_board[sub_game[0] // 3][sub_game[1] // 3] = current_player
                    print_board(board)
                    print(f"Player {current_player} wins sub-game at {(sub_game[0] // 3)+1}, {(sub_game[1] // 3)+1}!\n")
                    print_outer_board(outer_board)
                    
                    if check_board(outer_board, 0, 0):
                        print(f"Player {current_player} wins the game!\n")
                        break
                
                
            current_player = "O" if current_player == "X" else "X"  # Switch player after each move
            
            next_sub_game_row = (x%3)*3
            next_sub_game_col = (y%3)*3
            sub_game = (next_sub_game_row, next_sub_game_col)
            
            
            try:
                for q in range(9):
                    for w in range(9):
                        if board[q][w] == ".":
                            raise StopIteration
                print("Its a tie!")
                break
            except StopIteration:
                pass
            
    
    
    client.close()
    
host_game("10.30.201.100",9999)