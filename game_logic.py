import math # <-- REQUIRED for math.inf in minimax

# --- Game Constants ---
HUMAN = "X"
COMPUTER = "O"

# Scores for the Minimax algorithm
scores = {
    COMPUTER: 1,  # AI winning is a good score
    HUMAN: -1,    # Human winning is a bad score
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
            return current_board[condition[0]]  # Returns 'X' or 'O'
    # Check for Draw
    if "" not in current_board:
        return "Draw"
    return None # Game is still ongoing

def minimax(current_board, depth, is_maximizing):
    """The recursive Minimax algorithm."""
    # Note: This function uses 'scores', 'math.inf', 'HUMAN', and 'COMPUTER' 
    # which are all defined above or imported.
    
    result = check_win_state(current_board)
    
    # Base case: If game is over, return the score
    if result is not None:
        return scores[result]
        
    # Computer's turn (Maximizing)
    if is_maximizing:
        best_score = -math.inf
        empty_spots = [i for i, spot in enumerate(current_board) if spot == ""]
        for i in empty_spots:
            current_board[i] = COMPUTER
            score = minimax(current_board, depth + 1, False)
            current_board[i] = "" # Undo the move
            best_score = max(score, best_score)
        return best_score
        
    # Human's turn (Minimizing)
    else:
        best_score = math.inf
        empty_spots = [i for i, spot in enumerate(current_board) if spot == ""]
        for i in empty_spots:
            current_board[i] = HUMAN
            score = minimax(current_board, depth + 1, True)
            current_board[i] = "" # Undo the move
            best_score = min(score, best_score)
        return best_score

def find_best_move(current_board):
    """Finds the optimal move for the computer using Minimax."""
    # Note: This function uses 'COMPUTER' which is defined above.
    
    best_score = -math.inf
    best_move = -1
    
    empty_spots = [i for i, spot in enumerate(current_board) if spot == ""]
    for i in empty_spots:
        # 1. Make the move
        current_board[i] = COMPUTER
        
        # 2. Call Minimax (Human will try to minimize)
        score = minimax(current_board, 0, False)
        
        # 3. Undo the move
        current_board[i] = ""
        
        # 4. Check for the best score
        if score > best_score:
            best_score = score
            best_move = i
            
    return best_move