import math

# --- Game Constants ---
HUMAN = "X"
COMPUTER = "O"

# Scores for the Minimax algorithm
scores = {
    COMPUTER: 1,
    HUMAN: -1,
    "Draw": 0
}

# --- Core Game Functions ---

def check_win_state(current_board):
    """Checks if the given board state results in a win or draw."""
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    # Check for Winner
    for condition in win_conditions:
        if current_board[condition[0]] == current_board[condition[1]] == current_board[condition[2]] != "":
            return current_board[condition[0]]
    # Check for Draw
    if "" not in current_board:
        return "Draw"
    return None

def minimax(current_board, depth, is_maximizing):
    """The recursive Minimax algorithm."""
    result = check_win_state(current_board)
    
    if result is not None:
        return scores[result]
        
    if is_maximizing:
        best_score = -math.inf
        empty_spots = [i for i, spot in enumerate(current_board) if spot == ""]
        for i in empty_spots:
            current_board[i] = COMPUTER
            score = minimax(current_board, depth + 1, False)
            current_board[i] = ""
            best_score = max(score, best_score)
        return best_score
        
    else:
        best_score = math.inf
        empty_spots = [i for i, spot in enumerate(current_board) if spot == ""]
        for i in empty_spots:
            current_board[i] = HUMAN
            score = minimax(current_board, depth + 1, True)
            current_board[i] = ""
            best_score = min(score, best_score)
        return best_score

def find_best_move(current_board):
    """Finds the optimal move for the computer using Minimax."""
    best_score = -math.inf
    best_move = -1
    
    empty_spots = [i for i, spot in enumerate(current_board) if spot == ""]
    for i in empty_spots:
        current_board[i] = COMPUTER
        score = minimax(current_board, 0, False)
        current_board[i] = ""
        
        if score > best_score:
            best_score = score
            best_move = i
            
    return best_move
