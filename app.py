import streamlit as st
# FIX: Ensure all constants (HUMAN, COMPUTER) and functions are imported.
from game_logic import check_win_state, find_best_move, HUMAN, COMPUTER 

# --- Initialization and State Management ---

# Use Streamlit's session state to store the game board and turn
if 'board' not in st.session_state:
    st.session_state.board = [""] * 9
if 'current_player' not in st.session_state:
    st.session_state.current_player = HUMAN
if 'game_over' not in st.session_state:
    st.session_state.game_over = False

def reset_game():
    """Resets the board state and starts a new game."""
    st.session_state.board = [""] * 9
    st.session_state.current_player = HUMAN
    st.session_state.game_over = False
    st.rerun()

# --- Game Logic Functions for Streamlit ---

def handle_human_move(i):
    """Handles human click and prepares for the AI move."""
    board = st.session_state.board
    
    # 1. Check if the spot is empty and game is not over
    if board[i] == "" and st.session_state.current_player == HUMAN and not st.session_state.game_over:
        board[i] = HUMAN
        
        # 2. Check for game end immediately after human move
        winner = check_win_state(board)
        if winner:
            st.session_state.game_over = True
        else:
            # 3. If game continues, switch player to Computer
            st.session_state.current_player = COMPUTER
        
        st.rerun()

def ai_move():
    """Calculates and executes the AI's move."""
    board = st.session_state.board
    
    # Check if there are moves left and game is not over
    if "" in board and not st.session_state.game_over:
        # Find the best move
        move_index = find_best_move(board)
        
        if move_index != -1:
            # Execute the move and switch back to human
            board[move_index] = COMPUTER
            st.session_state.current_player = HUMAN
            
            # Check for game end after AI move
            winner = check_win_state(board)
            if winner:
                st.session_state.game_over = True
                
# --- Streamlit UI Layout ---

st.set_page_config(page_title="Minimax Tic-Tac-Toe", layout="centered")
st.title("Tic-Tac-Toe (Human vs. Minimax AI) 🤖")

# Create a 3x3 grid layout using Streamlit columns
for i in range(3):
    # Use 3 columns for each row
    cols = st.columns(3)
    for j in range(3):
        index = i * 3 + j
        board_value = st.session_state.board[index]
        
        # Prepare the button display text and color
        if board_value == "":
            label = " "
        else:
            label = board_value
            
        # Button is disabled if spot is taken OR game is over
        is_disabled = board_value != "" or st.session_state.game_over or st.session_state.current_player == COMPUTER

        # Use markdown and style for a large, colored symbol
        display_text = f"**<p style='font-size: 40px; color: {'red' if board_value == HUMAN else 'blue'}'>{label}</p>**"
        
        with cols[j]:
            st.button(
                display_text,
                key=f"btn_{index}",
                disabled=is_disabled,
                on_click=handle_human_move,
                args=(index,),
                use_container_width=True,
                unsafe_allow_html=True
            )

# --- AI Turn and Game End Handling ---

# If it's the AI's turn, calculate the move and force a refresh to display it
if st.session_state.current_player == COMPUTER and not st.session_state.game_over:
    st.info("AI is thinking...")
    # Use st.spinner for a nice loading effect while the AI calculates 
    with st.spinner('Calculating best move...'):
        ai_move() 
    st.rerun() # Force a refresh to show the AI's move and switch back to the human

# Display Game End Message and Reset Button
winner = check_win_state(st.session_state.board)
if st.session_state.game_over:
    if winner == HUMAN:
        st.success(f"🎉 **{HUMAN} wins! (You beat the AI!)**")
    elif winner == COMPUTER:
        st.error(f"🤖 **{COMPUTER} wins! (AI is tough!)**")
    elif winner == "Draw":
        st.info("🤝 **It's a draw!**")
        
    st.button("Start New Game", on_click=reset_game)

st.caption("Developed with Python and Streamlit.")