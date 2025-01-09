from collections import deque
from player import Player
from board import Board
from utils.dice import roll_dice

class SnakesAndLadders:
    def __init__(self, board, players):
        self.board = board
        self.players = deque(players)  # Queue for round-robin turns

    def play_turn(self):
        # Get the current player (FIFO from the queue)
        current_player = self.players.popleft()

        self.last_roll = roll_dice()  # Store the last roll

        # Move the player
        new_position = current_player.move(self.last_roll)

        # Check for snake or ladder
        final_position = self.board.check_position(new_position)
        if new_position != final_position:
            current_player.set_position(final_position)

        # Check if the player has won
        if current_player.position == 100:
            return current_player

        # Add the player back to the queue for the next turn
        self.players.append(current_player)
        return None
