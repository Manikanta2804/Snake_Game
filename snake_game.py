import turtle
import time
import random
from tkinter import messagebox
from tkinter.simpledialog import askstring
from PIL import Image

# Global Variables
score = 0
high_score = 0
delay = 0.1
player_name = ""
segments = []
speed_levels = {1: 0.2, 2: 0.1, 3: 0.05}  # 1: Slow, 2: Medium, 3: Fast

# Create the screen
win = turtle.Screen()
win.title("Snake Game")
win.bgcolor("black")
win.setup(width=800, height=600)  # Increased width for instructions
win.tracer(0)

# Draw visible border/wall
border = turtle.Turtle()
border.speed(0)
border.color("white")
border.penup()
border.goto(-290, -290)
border.pendown()
border.pensize(3)
for _ in range(4):
    border.forward(580)
    border.left(90)
border.hideturtle()

# Score Display
score_display = turtle.Turtle()
score_display.speed(0)
score_display.color("white")
score_display.penup()
score_display.hideturtle()
score_display.goto(0, 260)

# Instructions Display
instructions_display = turtle.Turtle()
instructions_display.speed(0)
instructions_display.color("white")
instructions_display.penup()
instructions_display.hideturtle()
instructions_display.goto(320, 150)  # Move instructions to the right side

# Display Instructions
def show_instructions():
    instructions = (
        "Instructions:\n"
        "1. Use arrow keys to move.\n"
        "2. Eat blue food to grow.\n"
        "3. Avoid walls and tail.\n"
        "4. Game ends if you hit the wall or yourself."
    )
    instructions_display.clear()
    instructions_display.write(instructions, align="left", font=("Courier", 12, "normal"))

# Welcome Screen
def welcome_screen():
    response = messagebox.askyesno("Snake Game", "1. Start Game\n2. Exit\nChoose 'Yes' to Start or 'No' to Exit.")
    if response:
        show_image()
    else:
        win.bye()

# Show Image
def show_image():
    try:
        img = Image.open("assets/snake.jpg")
        img.show()
    except FileNotFoundError:
        print("Image 'snake.jpg' not found in the assets folder.")
    get_username()

# Get Username
def get_username():
    global player_name
    player_name = askstring("Welcome to Snake Game", "Enter your name:")
    if not player_name:
        player_name = "Player"
    response = messagebox.askokcancel(f"Hey {player_name}", "Have fun! Press OK to continue.")
    if response:
        select_speed()
    else:
        win.bye()

# Select Speed Level
def select_speed():
    global delay, selected_speed
    speed = messagebox.askquestion("Speed Level", "Choose Speed:\nYes for Slow\nNo for Fast")
    selected_speed = speed_levels[1] if speed == 'yes' else speed_levels[3]
    delay = selected_speed  # Use this instead of setting a fixed value
    start_game()

# Start Game
def start_game():
    global head, food, segments

    # Clear previous snake segments
    for segment in segments:
        segment.goto(1000, 1000)  # Move segments off-screen
    segments.clear()

    # Snake Head
    head = turtle.Turtle()
    head.speed(0)
    head.shape("square")
    head.color("green")
    head.penup()
    head.goto(0, 0)
    head.direction = "stop"

    # Food
    food = turtle.Turtle()
    food.speed(0)
    food.shape("circle")
    food.color("blue")
    food.penup()
    food.goto(0, 100)

    # Initial Score Display
    update_score_display()
    show_instructions()

    # Keyboard Bindings
    win.listen()
    win.onkey(go_up, "Up")
    win.onkey(go_down, "Down")
    win.onkey(go_left, "Left")
    win.onkey(go_right, "Right")

    game_loop()

# Update Score Display
def update_score_display():
    score_display.clear()
    score_display.write(
        f"Player: {player_name}  Score: {score}  High Score: {high_score}", align="center", font=("Courier", 16, "normal")
    )

# Functions to Move the Snake
def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

def move():
    if head.direction == "up":
        head.sety(head.ycor() + 20)
    if head.direction == "down":
        head.sety(head.ycor() - 20)
    if head.direction == "left":
        head.setx(head.xcor() - 20)
    if head.direction == "right":
        head.setx(head.xcor() + 20)

# Game Loop
def game_loop():
    global score, high_score, delay
    while True:
        win.update()

        # Check for collision with the wall
        if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
            end_game()
            break

        # Check for collision with the food
        if head.distance(food) < 20:
            x = random.randint(-290, 290)
            y = random.randint(-290, 290)
            food.goto(x, y)

            # Add a segment
            new_segment = turtle.Turtle()
            new_segment.speed(0)
            new_segment.shape("square")
            new_segment.color("green")
            new_segment.penup()
            segments.append(new_segment)

            score += 10
            if score > high_score:
                high_score = score

            update_score_display()

            delay -= 0.001

        # Move the end segments first in reverse order
        for index in range(len(segments) - 1, 0, -1):
            x = segments[index - 1].xcor()
            y = segments[index - 1].ycor()
            segments[index].goto(x, y)

        # Move segment 0 to the head's position
        if len(segments) > 0:
            x = head.xcor()
            y = head.ycor()
            segments[0].goto(x, y)

        move()

        # Check for collision with the body
        for segment in segments:
            if segment.distance(head) < 20:
                end_game()
                return

        time.sleep(delay)

# End Game
def end_game():
    global score
    head.hideturtle()  # Hide the head when game over

    # Custom messages based on score
    if score == 0:
        message = "Oh no! Come back with a good score next time. Continue?"
    elif score < 50:
        message = f"Not bad! You scored {score}. Try to reach a higher score! Continue?"
    elif score < 100:
        message = f"Good effort! Your score: {score}. Can you hit 100 next time? Continue?"
    elif score < 200:
        message = f"Great job! You scored {score}. Aim for 200+ next round! Continue?"
    else:
        message = f"Amazing! You scored {score}. Keep up the great work! Continue?"

    response = messagebox.askyesno("Game Over", message)
    if response:
        reset_game()
    else:
        win.bye()

# Reset Game
def reset_game():
    global score, segments, delay
    score = 0
    delay = selected_speed  # Restore selected speed

    # Hide and remove all previous segments
    for segment in segments:
        segment.hideturtle()
    segments.clear()

    # Reset head position and show it again
    head.goto(0, 0)
    head.direction = "stop"
    head.showturtle()  # Make sure head is visible again

    update_score_display()
    game_loop()


# Start the game
welcome_screen()
win.mainloop()
