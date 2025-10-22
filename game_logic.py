# game_logic.py file
from typing import List, Optional

class SOSGame:
    def __init__(self, board_size: int = 3, mode: str = "simple"):
        """
        Initialize the game with a board size and mode.
        Mode can be 'simple' or 'general'.
        """
        self.board_size = max(3, int(board_size))  # Minimum board size is 3
        self.mode = mode if mode in ("simple", "general") else "simple"
        self.reset_game()  # Initialize the board and scores

    def set_board_size(self, size: int):
        """Set the board size and reset the game."""
        size = int(size)
        if size < 3:
            raise ValueError("Board size must be >= 3")
        self.board_size = size
        self.reset_game()

    def set_mode(self, mode: str):
        """Set the game mode."""
        if mode not in ("simple", "general"):
            raise ValueError("Mode must be 'simple' or 'general'")
        self.mode = mode

    def reset_game(self):
        """Reset the game board, scores, move count, and current turn."""
        self.board: List[List[Optional[str]]] = [
            [None for _ in range(self.board_size)] for _ in range(self.board_size)
        ]
        self.current_turn = "blue"
        self.move_count = 0
        self.scores = {"blue": 0, "red": 0}

    def in_bounds(self, r, c):
        """Check if the coordinates are within the board boundaries."""
        return 0 <= r < self.board_size and 0 <= c < self.board_size

    def cell_empty(self, r, c):
        """Check if a cell is empty and within bounds."""
        return self.in_bounds(r, c) and self.board[r][c] is None

    def make_move(self, r, c, letter: str) -> bool:
        """
        Place 'S' or 'O' on the board.
        Returns True if move was successful, False otherwise.
        Handles scoring in general mode and toggles turn in simple mode.
        """
        letter = (letter or "").strip().upper()
        if letter not in ("S", "O"):  # Validate input
            return False
        if not self.cell_empty(r, c):  # Check if cell is already occupied
            return False

        self.board[r][c] = letter
        self.move_count += 1  # Increment move count for each valid move

        # Check for SOS in general mode
        sos_found = self.check_for_sos(r, c) if self.mode == "general" else 0
        if sos_found:
            self.scores[self.current_turn] += sos_found
            # Keep the turn if SOS is found
        else:
            self.toggle_turn()  # Change turn if no SOS found
        return True

    def toggle_turn(self):
        """Switch the current turn to the other player."""
        self.current_turn = "red" if self.current_turn == "blue" else "blue"

    def get_cell(self, r, c):
        """Return the letter in a cell, or None if out of bounds."""
        if not self.in_bounds(r, c):
            return None
        return self.board[r][c]

    def get_board(self):
        """Return the current state of the board (for testing/debugging)."""
        return self.board

    def is_board_full(self):
        """Return True if all cells are filled."""
        return self.move_count >= self.board_size * self.board_size

    def check_for_sos(self, r, c) -> int:
        """
        Count how many SOS sequences were formed by the last move.
        Checks all four directions (horizontal, vertical, two diagonals).
        """
        directions = [
            (0, 1),   # right
            (1, 0),   # down
            (1, 1),   # diagonal down-right
            (1, -1),  # diagonal down-left
        ]
        count = 0
        for dr, dc in directions:
            # Check forward direction
            if self.form_sos(r, c, dr, dc):
                count += 1
            # Check backward direction
            if self.form_sos(r, c, -dr, -dc):
                count += 1
        return count

    def form_sos(self, r, c, dr, dc) -> bool:
        """
        Check if there is an 'S-O-S' pattern starting from (r, c)
        in the given direction (dr, dc).
        """
        if not (self.in_bounds(r, c) and
                self.in_bounds(r + dr, c + dc) and
                self.in_bounds(r + 2 * dr, c + 2 * dc)):
            return False
        return (
            self.board[r][c] == "S" and
            self.board[r + dr][c + dc] == "O" and
            self.board[r + 2 * dr][c + 2 * dc] == "S"
        )
