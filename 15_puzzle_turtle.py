import turtle
import tkinter as tk
import random

NUM_ROWS = 4  # Max 4
NUM_COLS = 4  # Max 4
TILE_WIDTH = 90  # Actual image size
TILE_HEIGHT = 90  # Actual image size
FONT_SIZE = 24
FONT = ('Helvetica', FONT_SIZE, 'normal')
SCRAMBLE_DEPTH = 100

images = []
for i in range(NUM_ROWS * NUM_COLS - 1):
    file = f"number-images/{i+1}.gif" # Use `.format()` instead if needed.
    images.append(file)

images.append("number-images/empty.gif")
images.append("number-images/scramble.gif")


def register_images():
    global screen
    for i in range(len(images)):
        screen.addshape(images[i])


def index_2d(my_list, v):
    """Returns the position of an element in a 2D list."""
    for i, x in enumerate(my_list):
        if v in x:
            return (i, x.index(v))


def swap_tile(tile):
    """Swaps the position of the clicked tile with the empty tile."""
    global screen

    current_i, current_j = index_2d(board, tile)
    empty_i, empty_j = find_empty_square_pos()
    empty_square = board[empty_i][empty_j]

    if is_adjacent([current_i, current_j], [empty_i, empty_j]):
        temp = board[empty_i][empty_j]
        board[empty_i][empty_j] = tile
        board[current_i][current_j] = temp

        draw_board()


def is_adjacent(el1, el2):
    """Determines whether two elements in a 2D array are adjacent."""
    if abs(el2[1] - el1[1]) == 1 and abs(el2[0] - el1[0]) == 0:
        return True
    if abs(el2[0] - el1[0]) == 1 and abs(el2[1] - el1[1]) == 0:
        return True
    return False


def find_empty_square_pos():
    """Returns the position of the empty square."""
    global board
    for row in board:
        for candidate in row:
            if candidate.shape() == "number-images/empty.gif":
                empty_square = candidate

    return index_2d(board, empty_square)


def scramble_board():
    """Scrambles the board in a way that leaves it solvable."""
    global board, screen

    for i in range(SCRAMBLE_DEPTH):
        for row in board:
            for candidate in row:
                if candidate.shape() == "number-images/empty.gif":
                    empty_square = candidate

        empty_i, empty_j = find_empty_square_pos()
        directions = ["up", "down", "left", "right"]

        if empty_i == 0: directions.remove("up")
        if empty_i >= NUM_ROWS - 1: directions.remove("down")
        if empty_j == 0: directions.remove("left")
        if empty_j >= NUM_COLS - 1: directions.remove("right")

        direction = random.choice(directions)

        if direction == "up": swap_tile(board[empty_i - 1][empty_j])
        if direction == "down": swap_tile(board[empty_i + 1][empty_j])
        if direction == "left": swap_tile(board[empty_i][empty_j - 1])
        if direction == "right": swap_tile(board[empty_i][empty_j + 1])


def draw_board():
    global screen, board

    # Disable animation
    screen.tracer(0)

    for i in range(NUM_ROWS):
        for j in range(NUM_COLS):
            tile = board[i][j]
            tile.showturtle()
            tile.goto(-138 + j * (TILE_WIDTH + 2), 138 - i * (TILE_HEIGHT + 2))

    # Restore animation
    screen.tracer(1)


def create_tiles():
    """
    Creates and returns a 2D list of tiles based on turtle objects
    in the winning configuration.
    """
    board = [["#" for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

    for i in range(NUM_ROWS):
        for j in range(NUM_COLS):
            tile_num = NUM_COLS * i + j
            tile = turtle.Turtle(images[tile_num])
            tile.penup()
            board[i][j] = tile

            def click_callback(x, y, tile=tile):
                """Passes `tile` to `swap_tile()` function."""
                return swap_tile(tile)

            tile.onclick(click_callback)

    return board


def create_scramble_button():
    """Uses a turtle with an image as a button."""
    global screen
    print(images)
    button = turtle.Turtle(images[NUM_ROWS * NUM_COLS])
    button.penup()
    button.goto(0, -240)
    button.onclick(lambda x, y: scramble_board())


def create_scramble_button_tkinter():
    """An alternative approach to creating a button using Tkinter."""
    global screen
    canvas = screen.getcanvas()
    button = tk.Button(canvas.master, text="Scramble", background="cadetblue", foreground="white", bd=0,
                       command=scramble_board)
    canvas.create_window(0, -240, window=button)


def main():
    global screen, board

    # Screen setup
    screen = turtle.Screen()
    screen.setup(600, 600)
    screen.title("15 Puzzle")
    screen.bgcolor("aliceblue")
    screen.tracer(0)  # Disable animation
    register_images()

    # Initialise game and display
    board = create_tiles()
    create_scramble_button_tkinter()
    # create_scramble_button()
    scramble_board()
    draw_board()
    screen.tracer(1)  # Restore animation


main()
turtle.done()
