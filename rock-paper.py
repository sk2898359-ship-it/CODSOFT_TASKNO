import random
import tkinter as tk
from tkinter import messagebox

CHOICES = ["Rock", "Paper", "Scissors"]


class RockPaperScissorsApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Rock-Paper-Scissors Game")
        self.root.geometry("520x500")
        self.root.resizable(False, False)
        self.root.configure(bg="#f1f5f9")

        # Game scores
        self.user_score = 0
        self.computer_score = 0
        self.ties = 0

        self.setup_ui()

    def setup_ui(self):
        # Header banner
        header = tk.Label(
            self.root,
            text="Rock Paper Scissors",
            font=("Arial", 16, "bold"),
            bg="#1e293b",
            fg="white",
            pady=12,
        )
        header.pack(fill=tk.X)

        # Instructions
        instruction_label = tk.Label(
            self.root,
            text="Choose Rock, Paper, or Scissors to play against the computer:",
            font=("Arial", 10),
            bg="#f1f5f9",
            fg="#475569",
            pady=8,
        )
        instruction_label.pack()

        # Selection Buttons
        btn_frame = tk.Frame(self.root, bg="#f1f5f9", pady=10)
        btn_frame.pack()

        tk.Button(
            btn_frame,
            text="Rock",
            font=("Arial", 11, "bold"),
            bg="#3b82f6",
            fg="white",
            width=10,
            pady=6,
            relief="flat",
            cursor="hand2",
            command=lambda: self.play_round("Rock"),
        ).grid(row=0, column=0, padx=8)

        tk.Button(
            btn_frame,
            text="Paper",
            font=("Arial", 11, "bold"),
            bg="#10b981",
            fg="white",
            width=10,
            pady=6,
            relief="flat",
            cursor="hand2",
            command=lambda: self.play_round("Paper"),
        ).grid(row=0, column=1, padx=8)

        tk.Button(
            btn_frame,
            text="Scissors",
            font=("Arial", 11, "bold"),
            bg="#f59e0b",
            fg="white",
            width=10,
            pady=6,
            relief="flat",
            cursor="hand2",
            command=lambda: self.play_round("Scissors"),
        ).grid(row=0, column=2, padx=8)

        # Round Results Display
        display_frame = tk.LabelFrame(
            self.root,
            text=" Round Results ",
            font=("Arial", 10, "bold"),
            bg="#ffffff",
            padx=15,
            pady=15,
        )
        display_frame.pack(fill=tk.X, padx=25, pady=12)

        self.user_choice_label = tk.Label(
            display_frame,
            text="Your Choice: -",
            font=("Arial", 11),
            bg="#ffffff",
            anchor="w",
        )
        self.user_choice_label.pack(fill=tk.X, pady=2)

        self.comp_choice_label = tk.Label(
            display_frame,
            text="Computer's Choice: -",
            font=("Arial", 11),
            bg="#ffffff",
            anchor="w",
        )
        self.comp_choice_label.pack(fill=tk.X, pady=2)

        self.outcome_label = tk.Label(
            display_frame,
            text="Make a move to start!",
            font=("Arial", 13, "bold"),
            bg="#ffffff",
            fg="#64748b",
            pady=8,
        )
        self.outcome_label.pack()

        # Scoreboard
        score_frame = tk.LabelFrame(
            self.root,
            text=" Scoreboard ",
            font=("Arial", 10, "bold"),
            bg="#ffffff",
            padx=15,
            pady=10,
        )
        score_frame.pack(fill=tk.X, padx=25, pady=6)

        self.score_display = tk.Label(
            score_frame,
            text="You: 0   |   Computer: 0   |   Ties: 0",
            font=("Arial", 11, "bold"),
            bg="#ffffff",
            fg="#1e293b",
        )
        self.score_display.pack(pady=4)

        # Control Buttons
        control_frame = tk.Frame(self.root, bg="#f1f5f9", pady=12)
        control_frame.pack()

        tk.Button(
            control_frame,
            text="Play Again (Clear Round)",
            font=("Arial", 9, "bold"),
            bg="#64748b",
            fg="white",
            padx=8,
            pady=4,
            relief="flat",
            command=self.reset_round,
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            control_frame,
            text="Reset Scores",
            font=("Arial", 9, "bold"),
            bg="#ef4444",
            fg="white",
            padx=8,
            pady=4,
            relief="flat",
            command=self.reset_all_scores,
        ).pack(side=tk.LEFT, padx=5)

    def play_round(self, user_choice):
        # Generate computer selection
        computer_choice = random.choice(CHOICES)

        # Update selections text
        self.user_choice_label.config(text=f"Your Choice: {user_choice}")
        self.comp_choice_label.config(
            text=f"Computer's Choice: {computer_choice}"
        )

        # Determine winner
        if user_choice == computer_choice:
            self.ties += 1
            self.outcome_label.config(
                text="It's a Tie!", fg="#d97706"
            )
        elif (
            (user_choice == "Rock" and computer_choice == "Scissors")
            or (user_choice == "Scissors" and computer_choice == "Paper")
            or (user_choice == "Paper" and computer_choice == "Rock")
        ):
            self.user_score += 1
            self.outcome_label.config(
                text="You Win!", fg="#16a34a"
            )
        else:
            self.computer_score += 1
            self.outcome_label.config(
                text="Computer Wins!", fg="#dc2626"
            )

        # Refresh score display
        self.update_score_label()

    def update_score_label(self):
        self.score_display.config(
            text=f"You: {self.user_score}   |   Computer: {self.computer_score}   |   Ties: {self.ties}"
        )

    def reset_round(self):
        self.user_choice_label.config(text="Your Choice: -")
        self.comp_choice_label.config(text="Computer's Choice: -")
        self.outcome_label.config(
            text="Ready for next round!", fg="#64748b"
        )

    def reset_all_scores(self):
        confirm = messagebox.askyesno(
            "Reset Game", "Do you want to reset all scores back to 0?"
        )
        if confirm:
            self.user_score = 0
            self.computer_score = 0
            self.ties = 0
            self.update_score_label()
            self.reset_round()


if __name__ == "__main__":
    app_root = tk.Tk()
    game = RockPaperScissorsApp(app_root)
    app_root.mainloop()