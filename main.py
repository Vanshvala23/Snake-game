from player import Player
from board import Board
from game import SnakesAndLadders
from gui import SnakesAndLaddersGUI
import tkinter as tk

def run_text_game():
    print("\n=== Text Mode Snakes and Ladders ===")
    board = Board()
    player_names = input("Enter player names separated by commas: ").split(",")
    players = [Player(name.strip()) for name in player_names]
    game = SnakesAndLadders(board, players)

    winner = None
    while not winner:
        input("\nPress Enter to roll dice...")
        winner = game.play_turn()

def run_gui_game():
    print("\n=== GUI Mode Snakes and Ladders ===")
    print("Opening game window...")
    board = Board()
    players = [
        Player("Player 1", "red"),
        Player("Player 2", "blue")
    ]
    game = SnakesAndLadders(board, players)
    
    root = tk.Tk()
    gui = SnakesAndLaddersGUI(root, game)
    root.mainloop()

def main():
    print("Welcome to Snakes and Ladders!")
    print("1: Text Mode")
    print("2: GUI Mode")
    mode = input("Choose mode (1 or 2): ")
    
    if mode == "1":
        run_text_game()
    elif mode == "2":
        run_gui_game()
    else:
        print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()