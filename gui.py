import tkinter as tk
import random
import time
import math

class SnakesAndLaddersGUI:
    def __init__(self, window, game):
        self.window = window
        self.game = game
        self.window.title("Snakes and Ladders")
        self.window.geometry("600x600")
        self.board_size = 10
        self.cell_size = 50
        self.player_icons = []
        self.last_roll = 0
        self.create_widgets()
        self.update_status()

    def create_widgets(self):
        self.canvas = tk.Canvas(self.window, width=self.board_size * self.cell_size, height=self.board_size * self.cell_size)
        self.canvas.pack()
        self.draw_board()
        self.player_icons = []
        self.create_players()
        
        # Add player turn indicator
        self.turn_label = tk.Label(self.window, text="", font=('Arial', 12))
        self.turn_label.pack(pady=5)
        
        self.dice_label = tk.Label(self.window, text="Dice: -", font=('Arial', 14))
        self.dice_label.pack(pady=5)
        
        # Add player position labels
        self.player_positions = tk.Frame(self.window)
        self.player_positions.pack(pady=5)
        self.position_labels = {}
        for player in self.game.players:
            label = tk.Label(
                self.player_positions, 
                text=f"{player.name}: Position 1", 
                font=('Arial', 12),
                fg=player.color
            )
            label.pack()
            self.position_labels[player.name] = label
        
        self.roll_button = tk.Button(self.window, text="Roll Dice", command=self.roll_dice)
        self.roll_button.pack(pady=10)
        self.status_label = tk.Label(self.window, text="", font=('Arial', 14))
        self.status_label.pack(pady=10)

    def draw_board(self):
        for row in range(self.board_size):
            for col in range(self.board_size):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                color = "lightgray" if (row + col) % 2 == 0 else "white"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
                
                # Calculate cell number in zigzag pattern
                if (self.board_size - 1 - row) % 2 == 0:
                    # Left to right
                    cell_number = (self.board_size - row - 1) * self.board_size + col + 1
                else:
                    # Right to left
                    cell_number = (self.board_size - row) * self.board_size - col
                    
                self.canvas.create_text(x1 + self.cell_size / 2, y1 + self.cell_size / 2, text=str(cell_number))
        
        # Add method to draw snakes and ladders
        self.draw_snakes_and_ladders()

    def draw_snakes_and_ladders(self):
        # Draw ladders
        for start, end in self.game.board.ladders.items():
            self.draw_ladder(start, end)
        
        # Draw snakes
        for start, end in self.game.board.snakes.items():
            self.draw_snake(start, end)

    def draw_ladder(self, start, end):
        # Convert board positions to canvas coordinates
        start_x, start_y = self.get_board_coordinates(start)
        end_x, end_y = self.get_board_coordinates(end)
        
        # Draw main ladder lines
        self.canvas.create_line(start_x - 10, start_y, end_x - 10, end_y, fill="brown", width=3)
        self.canvas.create_line(start_x + 10, start_y, end_x + 10, end_y, fill="brown", width=3)
        
        # Draw rungs
        steps = int(((end_x - start_x)**2 + (end_y - start_y)**2)**0.5 / 20)
        for i in range(steps):
            t = i / (steps - 1)
            rung_x1 = start_x - 10 + (end_x - start_x) * t
            rung_y1 = start_y + (end_y - start_y) * t
            rung_x2 = start_x + 10 + (end_x - start_x) * t
            rung_y2 = start_y + (end_y - start_y) * t
            self.canvas.create_line(rung_x1, rung_y1, rung_x2, rung_y2, fill="brown", width=2)

    def draw_snake(self, start, end):
        # Get coordinates for start and end positions
        start_x, start_y = self.get_board_coordinates(start)
        end_x, end_y = self.get_board_coordinates(end)
        
        # Create snake curve points with multiple control points for better curves
        dx = end_x - start_x
        dy = end_y - start_y
        
        # Create two control points for better curves
        ctrl1_x = start_x + dx * 0.25 + (40 if dx < 0 else -40)
        ctrl1_y = start_y + dy * 0.25
        ctrl2_x = start_x + dx * 0.75 + (-40 if dx < 0 else 40)
        ctrl2_y = start_y + dy * 0.75
        
        # Draw snake body with smoother curve
        points = [
            start_x, start_y,
            ctrl1_x, ctrl1_y,
            ctrl2_x, ctrl2_y,
            end_x, end_y
        ]
        self.canvas.create_line(points, smooth=True, fill="green", width=5)
        
        # Draw snake head at the start position (higher number)
        self.canvas.create_oval(start_x-12, start_y-12, start_x+12, start_y+12, fill="darkgreen")
        # Draw snake eyes
        eye_offset = -1 if dx < 0 else 1  # Adjust eye direction based on snake orientation
        self.canvas.create_oval(start_x + (eye_offset * 5), start_y-5, 
                              start_x + (eye_offset * 2), start_y-2, fill="white")
        self.canvas.create_oval(start_x + (eye_offset * 5), start_y+2, 
                              start_x + (eye_offset * 2), start_y+5, fill="white")
        
        # Draw tail (smaller) at the end position
        self.canvas.create_oval(end_x-6, end_y-6, end_x+6, end_y+6, fill="lightgreen")

    def create_players(self):
        for player in self.game.players:
            # Create a more interesting player token (a circle with a border)
            x, y = self.get_board_coordinates(player.position)
            
            # Create border circle (slightly larger)
            border = self.canvas.create_oval(
                x - 17, y - 17, 
                x + 17, y + 17, 
                fill='white', 
                outline='black', 
                width=2
            )
            
            # Create inner circle
            token = self.canvas.create_oval(
                x - 15, y - 15, 
                x + 15, y + 15, 
                fill=player.color,
                outline=player.color
            )
            
            # Add player number/initial
            text = self.canvas.create_text(
                x, y,
                text=player.name[0],  # First letter of player name
                fill='white',
                font=('Arial', 12, 'bold')
            )
            
            # Store all components of the player token
            self.player_icons.append((border, token, text))

    def roll_dice(self):
        current_player = self.game.players[0]
        old_position = current_player.position
        winner = self.game.play_turn()
        
        # Update dice and position displays
        self.dice_label.config(text=f"Dice: {self.game.last_roll}")
        
        # Check if player hit a snake
        if old_position in self.game.board.snakes:
            self.animate_snake_movement(current_player, old_position, current_player.position)
        else:
            self.update_player_position(current_player)
        
        # Update position label for current player
        self.position_labels[current_player.name].config(
            text=f"{current_player.name}: Position {current_player.position}"
        )
        
        if winner:
            self.status_label.config(text=f"🎉 {winner.name} wins! 🎉")
            self.roll_button.config(state="disabled")
        else:
            self.update_status()

    def animate_snake_movement(self, player, start_pos, end_pos):
        player_index = list(self.position_labels.keys()).index(player.name)
        border, token, text = self.player_icons[player_index]
        
        # Get coordinates for start and end positions
        start_x, start_y = self.get_board_coordinates(start_pos)
        end_x, end_y = self.get_board_coordinates(end_pos)
        
        # Create animation frames
        frames = 30
        
        def get_bezier_point(t):
            # Create a curved path
            ctrl_x = (start_x + end_x) / 2 + (50 if start_x < end_x else -50)
            ctrl_y = (start_y + end_y) / 2
            x = (1-t)**2 * start_x + 2*(1-t)*t * ctrl_x + t**2 * end_x
            y = (1-t)**2 * start_y + 2*(1-t)*t * ctrl_y + t**2 * end_y
            return x, y
        
        def animate_frame(frame):
            if frame < frames:
                t = frame / frames
                x, y = get_bezier_point(t)
                
                # Add bouncing and spinning effects
                bounce = abs(math.sin(t * math.pi * 4)) * 10
                scale = 1 + abs(math.sin(t * math.pi * 2)) * 0.2
                
                # Update border position with scale
                self.canvas.coords(border,
                                 x - (17 * scale), y - (17 * scale) - bounce,
                                 x + (17 * scale), y + (17 * scale) - bounce)
                
                # Update token position with scale
                self.canvas.coords(token,
                                 x - (15 * scale), y - (15 * scale) - bounce,
                                 x + (15 * scale), y + (15 * scale) - bounce)
                
                # Update text position
                self.canvas.coords(text, x, y - bounce)
                
                # Flash effect
                if frame % 6 < 3:
                    self.canvas.itemconfig(token, fill='red')
                    self.canvas.itemconfig(text, fill='white')
                else:
                    self.canvas.itemconfig(token, fill=player.color)
                    self.canvas.itemconfig(text, fill='white')
                
                self.window.after(20, lambda: animate_frame(frame + 1))
            else:
                # Reset to normal appearance
                self.canvas.itemconfig(token, fill=player.color)
                self.canvas.itemconfig(text, fill='white')
                self.update_player_position(player)
        
        # Start animation
        self.window.after(0, lambda: animate_frame(0))

    def update_player_position(self, player):
        player_index = list(self.position_labels.keys()).index(player.name)
        x, y = self.get_board_coordinates(player.position)
        
        # Update all components of the player token
        border, token, text = self.player_icons[player_index]
        self.canvas.coords(border, x - 17, y - 17, x + 17, y + 17)
        self.canvas.coords(token, x - 15, y - 15, x + 15, y + 15)
        self.canvas.coords(text, x, y)

    def update_status(self):
        current_player = self.game.players[0]
        self.status_label.config(text=f"{current_player.name}'s turn")
        self.turn_label.config(text=f"Current Turn: {current_player.name}", fg=current_player.color)

    def get_board_coordinates(self, position):
        """Convert board position (1-100) to x,y coordinates"""
        position = position - 1  # Convert to 0-based position
        row = (self.board_size - 1) - (position // self.board_size)
        col = position % self.board_size
        
        # If row is odd from bottom, reverse column direction
        if ((self.board_size - 1) - row) % 2 == 1:  # Changed from 0 to 1
            col = self.board_size - 1 - col
        
        x = col * self.cell_size + self.cell_size / 2
        y = row * self.cell_size + self.cell_size / 2
        return x, y

if __name__ == "__main__":
    window = tk.Tk()
    snakes_ladders_game = SnakesAndLaddersGUI(window, None)
    window.mainloop()
