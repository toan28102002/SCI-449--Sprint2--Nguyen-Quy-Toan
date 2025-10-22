# main.py file
import tkinter as tk
from tkinter import ttk, messagebox
from game_logic import SOSGame


class SOSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SOS Game - Sprint 2")

        # Initialize game logic with default board size and mode
        self.game = SOSGame(board_size=3, mode="simple")

        # Create UI widgets and build the game board
        self.create_widgets()
        self.build_board_ui()

    def create_widgets(self):
        # Top frame holds player settings and controls
        top_frame = ttk.Frame(self.root, padding=8)
        top_frame.grid(row=0, column=0, sticky="ew")

        # ====== RED PLAYER ======
        red_frame = ttk.LabelFrame(top_frame, text="Red Player", padding=6)
        red_frame.grid(row=0, column=0, padx=(4, 20))
        self.red_letter_var = tk.StringVar(value="S")
        # Radio buttons to choose S or O for Red Player
        ttk.Radiobutton(red_frame, text="S", variable=self.red_letter_var, value="S").grid(row=0, column=0, padx=5)
        ttk.Radiobutton(red_frame, text="O", variable=self.red_letter_var, value="O").grid(row=0, column=1, padx=5)

        # ====== CENTER SETTINGS ======
        center_frame = ttk.Frame(top_frame)
        center_frame.grid(row=0, column=1)
        ttk.Label(center_frame, text="Board size:").grid(row=0, column=0, sticky="w")
        # Spinbox to select board size (3-12)
        self.size_var = tk.IntVar(value=self.game.board_size)
        ttk.Spinbox(center_frame, from_=3, to=12, width=5, textvariable=self.size_var).grid(row=0, column=1, padx=(5, 15))

        ttk.Label(center_frame, text="Game mode:").grid(row=0, column=2, sticky="w")
        self.mode_var = tk.StringVar(value=self.game.mode)
        # Radio buttons to choose game mode
        ttk.Radiobutton(center_frame, text="Simple", variable=self.mode_var, value="simple").grid(row=0, column=3)
        ttk.Radiobutton(center_frame, text="General", variable=self.mode_var, value="general").grid(row=0, column=4)
        # Button to start a new game with selected settings
        ttk.Button(center_frame, text="Start New Game", command=self.on_start_new_game).grid(row=0, column=5, padx=(15, 0))

        # ====== BLUE PLAYER ======
        blue_frame = ttk.LabelFrame(top_frame, text="Blue Player", padding=6)
        blue_frame.grid(row=0, column=2, padx=(20, 4))
        self.blue_letter_var = tk.StringVar(value="S")
        # Radio buttons to choose S or O for Blue Player
        ttk.Radiobutton(blue_frame, text="S", variable=self.blue_letter_var, value="S").grid(row=0, column=0, padx=5)
        ttk.Radiobutton(blue_frame, text="O", variable=self.blue_letter_var, value="O").grid(row=0, column=1, padx=5)

        # ====== Turn Label ======
        # Shows current player's turn
        self.turn_label = ttk.Label(self.root, text=f"Current turn: {self.game.current_turn}", font=("Arial", 11, "bold"))
        self.turn_label.grid(row=1, column=0, pady=(4, 4))

        # ====== Scoreboard (hidden for simple mode) ======
        # Displays current scores in general mode
        self.score_label = ttk.Label(self.root, text="", font=("Arial", 10, "bold"))
        self.score_label.grid(row=2, column=0, pady=(0, 4))

        # ====== Board Frame ======
        # Container for all the cell buttons
        self.board_frame = ttk.Frame(self.root, padding=8)
        self.board_frame.grid(row=3, column=0)

        # ====== Status Label ======
        # Shows game messages like invalid moves or placed letters
        self.status_label = ttk.Label(self.root, text="Click a cell to place S or O.", anchor="w")
        self.status_label.grid(row=4, column=0, sticky="ew", padx=8, pady=(4, 8))

    def build_board_ui(self):
        # Remove old buttons before rebuilding
        for w in self.board_frame.winfo_children():
            w.destroy()

        size = self.game.board_size
        # Create a 2D list to store button widgets
        self.cell_buttons = [[None for _ in range(size)] for _ in range(size)]

        for r in range(size):
            for c in range(size):
                btn = tk.Button(self.board_frame, text="", width=4, height=2,
                                font=("Arial", 12, "bold"),
                                command=lambda rr=r, cc=c: self.on_cell_clicked(rr, cc))
                btn.grid(row=r, column=c, padx=2, pady=2)
                self.cell_buttons[r][c] = btn

        # Update labels
        self.update_turn_label()
        self.update_score_label()

    def on_start_new_game(self):
        try:
            # Get user-selected board size and mode
            size = int(self.size_var.get())
            mode = self.mode_var.get()
            self.game.set_board_size(size)
            self.game.set_mode(mode)
            # Reset the game state
            self.game.reset_game()
            self.build_board_ui()
            self.status_label.config(text=f"Started {mode} game ({size}x{size})")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_cell_clicked(self, r, c):
        # Determine which player's letter to place
        letter = self.red_letter_var.get() if self.game.current_turn == "red" else self.blue_letter_var.get()
        if not self.game.make_move(r, c, letter):
            # Invalid move
            self.status_label.config(text=f"Invalid move at ({r},{c}). Try again.")
            return

        # Update UI after a valid move
        self.update_cell_ui(r, c)
        self.update_turn_label()
        self.update_score_label()
        self.status_label.config(text=f"{letter} placed by {self.previous_player()} at ({r},{c}).")

        # Check if board is full
        if self.game.is_board_full():
            self.end_game()

    def previous_player(self):
        # Return the player who played the previous turn
        return "red" if self.game.current_turn == "blue" else "blue"

    def update_cell_ui(self, r, c):
        # Update the visual display of a single cell
        val = self.game.get_cell(r, c)  # Get value from game board
        btn = self.cell_buttons[r][c]   # Get the corresponding button
        btn.config(text=val if val else "")  # Update text
        color = "red" if self.previous_player() == "red" else "blue"
        btn.config(fg=color)  # Set text color based on player

    def update_turn_label(self):
        # Update the turn label to current player
        self.turn_label.config(text=f"Current turn: {self.game.current_turn}")

    def update_score_label(self):
        # Update the score label if in general mode
        if self.game.mode == "general":
            self.score_label.config(
                text=f"Blue: {self.game.scores['blue']}   |   Red: {self.game.scores['red']}"
            )
        else:
            self.score_label.config(text="")  # Hide scores in simple mode

    def end_game(self):
        # Show game over message with winner or tie
        blue, red = self.game.scores["blue"], self.game.scores["red"]
        if self.game.mode == "simple":
            messagebox.showinfo("Game Over", "Board is full! Simple game ended.")
        else:
            if blue > red:
                msg = f"Blue wins! ({blue} - {red})"
            elif red > blue:
                msg = f"Red wins! ({red} - {blue})"
            else:
                msg = f"It's a tie! ({blue} - {red})"
            messagebox.showinfo("Game Over", msg)


def main():
    # Initialize Tkinter root window and start the game
    root = tk.Tk()
    app = SOSApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
