HUMAN = "X"
COMPUTER = "O"

def check_win_state(board):
    win_combos = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]
    for combo in win_combos:
        a, b, c = combo
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]

    if "" not in board:
        return "Draw"

    return None

def find_best_move(board):
    # Simple minimax (or just pick first available for demo)
    for i in range(9):
        if board[i] == "":
            return i
    return -1
