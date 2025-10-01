print("✅ This is the updated app.py file")

import streamlit as st
from game_logic import check_win_state, find_best_move, HUMAN, COMPUTER

# --- Initialization and State Management ---

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

# --- Game Logic Functions ---

def handle_human_move(i):
    """Handles human click and prepares for the AI move."""
    board = st.session_state.board

    if board[i] == "" and st.session_state.current_player == HUMAN and not st.session_state.game_over:
        board[i] = HUMAN
        winner = check_win_state(board)
        if winner:
            st.session_state.game_over = True
        else:
            st.session_state.current_player = COMPUTER
        st.rerun()

def ai_move():
    """Calculates and executes the AI's move."""
    board = st.session_state.board

    if "" in board and not st.session_state.game_over:
        move_index = find_best_move(board)
        if move_index != -1:
            board[move_index] = COMPUTER
            winner = check_win_state(board)
            if winner:
                st.session_state.game_over = True
            else:
                st.session_state.current_player = HUMAN

# --- Streamlit UI Layout ---

st.set_page_config(page_title="Minimax Tic-Tac-Toe", layout="centered")
st.title("Tic-Tac-Toe (Human vs. Minimax AI) 🤖")

# Create a 3x3 grid using columns
for i in range(3):
    cols = st.columns(3)
    for j in range(3):
        index = i * 3 + j
        value = st.session_state.board[index]

        # Emoji display for players
        if value == "":
            label = " "  # Empty
        elif value == HUMAN:
            label = "❌"
        else:
            label = "⭕"

        # Disable logic
        is_disabled = value != "" or st.session_state.game_over or st.session_state.current_player != HUMAN

        with cols[j]:
            st.button(
                label,
                key=f"btn_{index}",
                disabled=is_disabled,
                on_click=handle_human_move,
                args=(index,),
                use_container_width=True
            )

# --- AI Turn Logic ---

if st.session_state.current_player == COMPUTER and not st.session_state.game_over:
    st.info("AI is thinking...")
    with st.spinner("Calculating best move..."):
        ai_move()
    st.rerun()

# --- Game Result ---

winner = check_win_state(st.session_state.board)
if st.session_state.game_over:
    if winner == HUMAN:
        st.success("🎉 You win!")
    elif winner == COMPUTER:
        st.error("🤖 AI wins!")
    elif winner == "Draw":
        st.info("🤝 It's a draw!")

    st.button("🔁 Start New Game", on_click=reset_game)

st.caption("Developed with Python and Streamlit.")
