import tkinter as tk
from tkinter import messagebox
import math

# --- Game Constants and Initialization ---
root = tk.Tk()
root.title("Tic-Tac-Toe (Human vs. Minimax AI)")

HUMAN = "X"
COMPUTER = "O"
current_player = HUMAN
board = [""] * 9

# --- Minimax AI Logic (The Tougher Part) ---

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

# Scores for the Minimax algorithm
scores = {
    COMPUTER: 1,  # AI winning is a good score
    HUMAN: -1,    # Human winning is a bad score
    "Draw": 0
}

def minimax(current_board, depth, is_maximizing):
    """The recursive Minimax algorithm."""
    result = check_win_state(current_board)

    # Base case: If game is over, return the score based on who won
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

def computer_move():
    """Executes the computer's optimal move."""
    global current_player

    if current_player != COMPUTER:
        return

    # Find the best move using the minimax algorithm
    move_index = find_best_move(board)

    # Execute the move
    if move_index != -1:
        board[move_index] = COMPUTER
        buttons[move_index].config(text=COMPUTER, fg='blue')

        # Check for game end
        if check_game_end():
            return

        current_player = HUMAN


def check_game_end():
    """Checks for winner/draw and shows the messagebox."""
    winner = check_win_state(board)
    
    if winner == HUMAN:
        messagebox.showinfo("Game Over", f"{HUMAN} wins! (You beat the AI!)")
        reset_board()
        return True
    elif winner == COMPUTER:
        messagebox.showinfo("Game Over", f"{COMPUTER} wins! (AI is tough!)")
        reset_board()
        return True
    elif winner == "Draw":
        messagebox.showinfo("Game Over", "It's a draw!")
        reset_board()
        return True
    
    return False

def button_click(i):
    """Handles the human player's move."""
    global current_player
    
    # Check if it's the human's turn AND the spot is empty
    if board[i] == "" and current_player == HUMAN:
        # 1. Human makes a move
        board[i] = HUMAN
        buttons[i].config(text=HUMAN, fg='red') 
        
        # 2. Check if the human won
        if not check_game_end():
            # 3. If game continues, switch player to Computer
            current_player = COMPUTER
            
            # 4. Trigger the computer's move after a brief delay 
            root.after(500, computer_move) 

def reset_board():
    """Resets the board and game state."""
    global board, current_player
    board = [""] * 9
    current_player = HUMAN # Human always starts
    for button in buttons:
        button.config(text="", fg='black') 

# --- GUI Setup ---
buttons = []
for i in range(9):
    # Setup buttons with larger font/size for visibility
    button = tk.Button(root, text="", 
                       font=('Arial', 32, 'bold'), 
                       width=4, height=2,
                       command=lambda i=i: button_click(i),
                       relief=tk.RAISED, bd=5) 
    button.grid(row=i//3, column=i%3, padx=2, pady=2)
    buttons.append(button)

# Run the application
root.mainloop() 