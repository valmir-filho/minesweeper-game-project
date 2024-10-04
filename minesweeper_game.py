from tkinter import messagebox  # Import messagebox for pop-up dialogs.
import random  # Import random for generating random mine locations.
import tkinter as tk  # Import the Tkinter library for GUI creation.


class Minesweeper:


    def __init__(self, root, rows=10, cols=10, mines=10):
        """
        Initializes the Minesweeper game with a grid of buttons (rows x cols) and randomly placed mines.
        :param root: The main window for the game (Tkinter root window).
        :param rows: Number of rows in the grid.
        :param cols: Number of columns in the grid.
        :param mines: Number of mines to place in the grid.
        """
        self.root = root  # Main window.
        self.rows = rows  # Number of rows.
        self.cols = cols  # Number of columns.
        self.mines = mines  # Number of mines.
        self.buttons = {}  # Dictionary to hold button objects for each cell.
        self.mine_positions = []  # List to store positions of the mines.
        self.create_board()  # Method to create the button grid.
        self.place_mines()  # Method to place the mines randomly in the grid.


    def create_board(self):
        """Creates the grid of buttons where each button represents a cell in the Minesweeper grid."""
        for r in range(self.rows):  # Loop through each row.
            for c in range(self.cols):  # Loop through each column.
                # Create a button for each cell, assign click event.
                button = tk.Button(self.root, width=2, height=1, 
                                   command=lambda r=r, c=c: self.click(r, c))
                # Bind right-click for flagging the cell.
                button.bind('<Button-3>', lambda e, r=r, c=c: self.right_click(r, c))
                # Arrange button in the grid layout.
                button.grid(row=r, column=c)
                # Store the button in the dictionary with its coordinates as the key.
                self.buttons[(r, c)] = button


    def place_mines(self):
        """Randomly places mines on the grid."""
        self.mine_positions.clear()  # Clear the list of mines if restarting.
        while len(self.mine_positions) < self.mines:  # Loop until the required number of mines are placed.
            r = random.randint(0, self.rows - 1)  # Random row.
            c = random.randint(0, self.cols - 1)  # Random column.
            if (r, c) not in self.mine_positions:  # Ensure the position isn't already a mine.
                self.mine_positions.append((r, c))  # Add the mine position to the list.


    def click(self, r, c):
        """
        Handles the left-click event. If the clicked cell is a mine, the game ends. 
        If not, the cell displays the number of adjacent mines.
        :param r: Row of the clicked button.
        :param c: Column of the clicked button.
        """
        if (r, c) in self.mine_positions:  # If the clicked cell is a mine.
            self.buttons[(r, c)].config(text="*", bg="red")  # Display the mine and change background to red.
            self.game_over(False)  # Call game over method, player loses.
        else:
            mine_count = self.count_mines(r, c)  # Count the number of adjacent mines.
            self.buttons[(r, c)].config(text=str(mine_count), state="disabled")  # Display count and disable button.
            if mine_count == 0:  # If no adjacent mines.
                self.reveal_adjacent(r, c)  # Reveal adjacent cells.


    def count_mines(self, r, c):
        """
        Counts the number of mines adjacent to the clicked cell.
        :param r: Row of the clicked cell.
        :param c: Column of the clicked cell.
        :return: The number of adjacent mines.
        """
        count = 0  # Initialize mine count.
        # Loop through all adjacent cells (3x3 area around the clicked cell).
        for i in range(r-1, r+2):
            for j in range(c-1, c+2):
                if (i, j) in self.mine_positions:  # If an adjacent cell contains a mine.
                    count += 1  # Increment mine count.
        return count  # Return the total number of adjacent mines.


    def reveal_adjacent(self, r, c):
        """
        Recursively reveals adjacent cells if they do not contain mines.
        :param r: Row of the clicked cell.
        :param c: Column of the clicked cell.
        """
        # Loop through all adjacent cells (3x3 area around the clicked cell).
        for i in range(r-1, r+2):
            for j in range(c-1, c+2):
                # Check if the adjacent cell is within bounds and not already revealed.
                if 0 <= i < self.rows and 0 <= j < self.cols and self.buttons[(i, j)]["state"] == "normal":
                    self.click(i, j)  # Recursively click adjacent cells.


    def right_click(self, r, c):
        """
        Handles the right-click event for flagging a cell.
        :param r: Row of the flagged cell.
        :param c: Column of the flagged cell.
        """
        self.buttons[(r, c)].config(text="?", bg="yellow")  # Mark the cell with a flag (?).


    def game_over(self, won):
        """
        Ends the game, showing all mines and asking the player if they want to play again or exit.
        :param won: Boolean indicating if the player won or lost.
        """
        # Show all mines on the board.
        for r, c in self.mine_positions:
            self.buttons[(r, c)].config(text="*", bg="red")  # Display all mines in red.
        # Display message depending on win or loss.
        msg = "You Win!" if won else "Game Over!"
        # Ask the player if they want to play again.
        play_again = messagebox.askquestion("Game Over", f"{msg}\nDo you want to play again?", icon='question')

        if play_again == 'yes':  # If the player chooses to play again.
            self.reset_game()  # Reset the game.
        else:
            self.root.quit()  # Quit the game if the player chooses to exit.


    def reset_game(self):
        """
        Resets the game by clearing all button labels and repositioning the mines.
        """
        # Loop through all buttons and reset them to their default state.
        for r in range(self.rows):
            for c in range(self.cols):
                button = self.buttons[(r, c)]
                button.config(text="", bg="SystemButtonFace", state="normal")  # Reset button text, color, and state.
        self.place_mines()  # Place new mines on the board.

# Create the main window (Tkinter root window).
root = tk.Tk()
# Set the title of the window.
root.title("Minesweeper")
# Initialize the Minesweeper game.
game = Minesweeper(root)
# Run the Tkinter event loop (keeps the window open).
root.mainloop()
