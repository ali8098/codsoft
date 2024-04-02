import random
import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QDialog, QListWidget
class MainMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Menu")
        self.setGeometry(100, 100, 400, 200)
        layout = QVBoxLayout()
        play_button = QPushButton("Start Game")
        play_button.clicked.connect(self.start_game)
        layout.addWidget(play_button)
        scores_button = QPushButton("View Scores")
        scores_button.clicked.connect(self.view_scores)
        layout.addWidget(scores_button)
        self.setLayout(layout)
        self.scores = self.load_scores()  
    def start_game(self):
        self.game_window = RPSapp(self)
        self.game_window.show()
        self.hide()
    def view_scores(self):
        scores_dialog = ScoreDialog(self.scores)
        scores_dialog.exec_()
    def save_scores(self):
        with open("scores.json", "w") as f:
            json.dump(self.scores, f)
    def load_scores(self):
        try:
            with open("scores.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}  
class RPSapp(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Rock, Paper, Scissors")
        self.setGeometry(100, 100, 400, 200)
        self.layout = QVBoxLayout()
        self.result_label = QLabel("Choose an option to play")
        self.layout.addWidget(self.result_label)
        rock_button = QPushButton("Rock")
        rock_button.clicked.connect(lambda: self.play("ROCK"))
        self.layout.addWidget(rock_button)
        paper_button = QPushButton("Paper")
        paper_button.clicked.connect(lambda: self.play("PAPER"))
        self.layout.addWidget(paper_button)
        scissors_button = QPushButton("Scissors")
        scissors_button.clicked.connect(lambda: self.play("SCISSORS"))
        self.layout.addWidget(scissors_button)
        back_button = QPushButton("Back")
        back_button.clicked.connect(self.back_to_main_menu)
        self.layout.addWidget(back_button)
        self.setLayout(self.layout)
    def play(self, user_choice):
        computer_choice = random.choice(["ROCK", "PAPER", "SCISSORS"])
        if user_choice == computer_choice:
            result = "It's a tie!"
        elif (user_choice == "ROCK" and computer_choice == "SCISSORS") or \
             (user_choice == "PAPER" and computer_choice == "ROCK") or \
             (user_choice == "SCISSORS" and computer_choice == "PAPER"):
            result = "You Won!"
            self.parent.scores["You"] = self.parent.scores.get("You", 0) + 1  
        else:
            result = "Computer wins!"
            self.parent.scores["Computer"] = self.parent.scores.get("Computer", 0) + 1 
        self.result_label.setText(f"Your choice: {user_choice}\nComputer's choice: {computer_choice}\n{result}")
    def back_to_main_menu(self):
        self.parent.save_scores()  
        self.parent.show()
class ScoreDialog(QDialog):
    def __init__(self, scores):
        super().__init__()
        self.setWindowTitle("Scores")
        self.setGeometry(100, 100, 400, 300)
        layout = QVBoxLayout()
        scores_list = QListWidget()
        for player, score in scores.items():
            scores_list.addItem(f"{player}: {score}")
        layout.addWidget(scores_list)
        back_button = QPushButton("Back")
        back_button.clicked.connect(self.close)
        layout.addWidget(back_button)
        self.setLayout(layout)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_menu = MainMenu()
    main_menu.show()
    sys.exit(app.exec_())
