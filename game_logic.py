HUMAN = "X"
COMPUTER = "O"

def check_win_state(board):
    """
    Checks the current state of the 3x3 board for a winner or a draw.
    Returns 'X', 'O', 'Draw', or None (game ongoing).
    """
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

# ----------------- Minimax Core Logic -----------------

def minimax(board, depth, is_maximizing):
    """
    The Minimax algorithm. Returns the score of the board state.
    """
    result = check_win_state(board)

    # Base cases (terminal states): Assign scores and incorporate depth
    if result == COMPUTER:
        return 10 - depth  # COMPUTER wins: +score, favor faster wins
    if result == HUMAN:
        return depth - 10  # HUMAN wins: -score, penalize faster losses
    if result == "Draw":
        return 0

    # Maximizing player (COMPUTER 'O')
    if is_maximizing:
        best_score = -float('inf')
        for i in range(9):
            if board[i] == "":
                board[i] = COMPUTER
                score = minimax(board, depth + 1, False)
                board[i] = "" # Undo the move (backtrack)
                best_score = max(best_score, score)
        return best_score

    # Minimizing player (HUMAN 'X')
    else:
        best_score = float('inf')
        for i in range(9):
            if board[i] == "":
                board[i] = HUMAN
                score = minimax(board, depth + 1, True)
                board[i] = "" # Undo the move (backtrack)
                best_score = min(best_score, score)
        return best_score

def find_best_move(board):
    """
    Finds the optimal move for the COMPUTER using the Minimax algorithm.
    Returns the index (0-8) of the best move.
    """
    best_score = -float('inf')
    best_move = -1

    # Check if the board is empty (first move optimization)
    if all(cell == "" for cell in board):
        # Taking the center (index 4) or a corner is the optimal first move.
        return 4 

    for i in range(9):
        if board[i] == "":
            board[i] = COMPUTER
            # Start with the minimizing step because the move 'i' has been made
            score = minimax(board, 0, False) 
            board[i] = ""

            if score > best_score:
                best_score = score
                best_move = i
            # If scores are equal, we can still update the move index 
            # (though the initial best_move will also be optimal)

    return best_move
