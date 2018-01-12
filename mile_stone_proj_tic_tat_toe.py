# no error checking anywhere

board = [[0,1,2], [3,4,5], [6,7,8]]


def print_board():
    for x in range(0,3):
        print '{a}|{b}|{c}'.format(a=board[x][0],b=board[x][1],c=board[x][2])
        if x < 2:
            print '-----'


def check_horizontal_winner(row):
    if board[row][0] == board[row][1] == board[row][2]:
        return True
    else:
        return False
        
    
def check_vertical_winner(col):
    if board[0][col] == board[1][col] == board[2][col]:
        return True
    else:
        return False
    
    
def check_diagonal_winner():
    # make simple check both
    if board[0][0] == board[1][1] == board[2][2] or board[0][2] == board[1][1] == board[2][0]:
        return True
    else:
        return False
    

def show_winner(player):
    print '\nGame over, player {a} wins.\n'.format(a=player)

    
    
def get_players_move(player):
    # no validation for this just learning 
    move = raw_input("Player {a} enter available position:".format(a=player))
    square = int(move)
    
    # update board
    col = square % 3
    row = square / 3
    board[row][col] = player
    
    # check for winner
    # always check horizontal and vertical
    if check_horizontal_winner(row):
        show_winner(player)
        return False
    
    if check_vertical_winner(col):
        show_winner(player)
        return False
    
    if row in (0,2) or col in (0,2) or (row == 1 and col == 1):
        if check_diagonal_winner():
            show_winner(player)
            return False
    
    
    return True
    
    
print_board()
keepGoing = True
x = 0

while keepGoing:
    player = 'Y'
    
    if x % 2 == 0:
        player = 'X'
        
    keepGoing = get_players_move(player)
    print_board()
    x += 1
    
    if x == 8:
        print 'End, Stalemate'
        keepGoing = False

