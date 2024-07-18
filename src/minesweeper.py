# Max: 30x30 24 mines
# Min: 9x9 10 mines
# Easy: 9x9 10 mines
# Medium: 16x30 40 mines
# Hard: 24x30 160 mines

# Drawing Mines:
# Create a list with 81 boxes using random.choices(["[ ]", "[X]"], k=10)
# Then break it down in its corresponding rows and columns

import random
import os
import keyboard
from time import sleep

def clear():
    os.system('clear')

class Difficulty:
    def __init__(self, rows: int, cols: int, mines: int):
        self.rows = rows
        self.cols = cols
        self.mines = mines

class Tile:
    def __init__(self, x: int, y: int, is_mine = False):
        self.x = x
        self.y = y
        self.is_mine = is_mine
        self.is_marked = False
        self.is_revealed = False
        self.is_selected = False
        
    def __str__(self):
        if (self.is_mine and self.is_revealed):
            return "[X]" if self.is_selected else "[x]"
        elif (self.is_revealed):
            return "[.]" if self.is_selected else "[]"
        elif (self.is_marked):
            return "[P]" if self.is_selected else "[p]"
        else: 
            return "[O]" if self.is_selected else "[0]"
        
    def mark(self):
        self.is_marked = True
        
    def reveal(self):
        self.is_revealed = True
        
    def select(self):
        self.is_selected = True
        
    def unselect(self):
        self.is_selected = False

DIFF_EASY = Difficulty(9, 9, 10)
DIFF_MEDIUM = Difficulty(16, 30, 40)
DIFF_HARD = Difficulty(24, 30, 160)

def menu(): 
    print('''
        xXx Welcome to Minesweeper! xXx
    ---------------------------------------

    Choose the difficulty by entering one of the options below.
    You can also customize your own difficulty by entering the amount of rows, columns and mines.
    An alternative to this is to write custom(c) and enter in manually.

    - Easy(e): 9x9 grid, 10 mines
    - Medium(m): 16x30 grid, 40 mines
    - Hard(h): 24x30 grid, 160 mines
    - Custom(rows columns mines): Min 9x9 grid, 10 mines and Max 30x30 grid, 240 mines
    - Quit(q): Quit the game
    ''')

    diff_choice = input("Difficulty: ")
    difficulty = Difficulty(0, 0, 0)

    match diff_choice.lower():
        case "easy" | "e":
            print("Playing with Easy difficulty")
            difficulty = DIFF_EASY

        case "medium" | "mid" | "m":
            print("Playing with Medium difficulty")
            difficulty = DIFF_MEDIUM

        case "hard" | "h":
            print("Playing with Hard Difficulty")
            difficulty = DIFF_HARD
            
        case "quit" | "q":
            if input("Do you want to quit the game? Y/N").lower() == "y":
                exit()
                
        case _:
            if (diff_choice.isnumeric() or ("custom" or "c" in diff_choice)):
                choices = [int(i) for i in diff_choice.split()]

                if (len(choices) <= 3):
                    difficulty.rows = choices[0] if choices[0] is not None else int(input("Amount of Rows (max 30): "))
                    difficulty.cols = choices[1] if len(choices) > 1 is not None else int(input("Amount of Columns (max 30): "))
                    difficulty.mines = choices[2] if len(choices) > 2 is not None else int(input("Amount of Mines (max 240): "))

            else:
                print("Choose a difficulty or create a custom difficulty by entering the amount of rows, columns and mines.")
                menu()
    return difficulty

def play_game(difficulty: Difficulty):
    tile_count = difficulty.rows * difficulty.cols

    grid = [[Tile(x = x, y = y) for x in range(difficulty.cols)] for y in range(difficulty.rows)]
    # player_grid = [row.copy() for row in master_grid]
    
    for mine in random.sample(range(0, tile_count - 1), difficulty.mines):
        r  = mine // difficulty.cols
        c = mine % difficulty.cols
        grid[r][c].is_mine = True

    def draw_grid():
        clear()
        print(f"Current Difficulty {difficulty.rows}x{difficulty.cols}, {difficulty.mines} mines.\n")
        print(f"x ", end = "")
        for i in range(difficulty.cols):
            print(f" {i} ", end = "")
            # print(f" {chr(97 + i)} ", end = "")
        print("")
        for row in grid:
            print(f"{grid.index(row)} ", end="")
            for col in row:
                print(col, end="")
            print("")
               
    if (difficulty.cols % 2 == 0 and difficulty.rows % 2 == 0):
        selected_tile = grid[0][0]
    else:
        selected_tile = grid[(difficulty.rows//2)][(difficulty.cols//2)]

    selected_tile.select()

    draw_grid()
    
    while True:
        user_input = keyboard.read_key()    
        print(selected_tile.x, selected_tile.y)  
        match user_input:
            case 'vänsterpil' | "left":
                if (selected_tile.x - 1 != -1):
                    selected_tile.unselect()
                    selected_tile = grid[selected_tile.y][selected_tile.x - 1]
                    selected_tile.select()
                else:
                    pass
                
            case 'högerpil' | 'right':
                if (selected_tile.x + 1 != difficulty.cols):
                    selected_tile.unselect()
                    selected_tile = grid[selected_tile.y][selected_tile.x + 1]
                    selected_tile.select()
                else:
                    pass
                
            case 'uppil' | "up":
                if (selected_tile.y - 1 != -1):
                    selected_tile.unselect()
                    selected_tile = grid[selected_tile.y - 1][selected_tile.x]
                    selected_tile.select()
                else:
                    pass
                
            case 'nedpil' | "down":
                if (selected_tile.y + 1 != difficulty.rows):
                    selected_tile.unselect()
                    selected_tile = grid[selected_tile.y + 1][selected_tile.x]
                    selected_tile.select()
                else:
                    pass
                
            case 'space':
                selected_tile.reveal()
                
            case 'skift' | "shift":
                selected_tile.mark()
        
        draw_grid()
        print(selected_tile.x, selected_tile.y)  
        
            

    play_again = input("\nDo you want to play again? Y/N: ")
    if play_again.lower() == "y":
        play_game(difficulty)

while True:
    clear()
    difficulty = menu()
    clear()
    play_game(difficulty)
    sleep(5)

# while True:
#     if keyboard.read_key() == "q":
#         print("Do you want to quit the game Y/N?")
#         if keyboard.read_key() == "Y":
#             exit()