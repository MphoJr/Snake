import tkinter as tk
import random

# Game settings
WIDTH = 400
HEIGHT = 400
CELL_SIZE = 20

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack()

        # Difficulty selector
        self.speed = 150  # default
        self.difficulty_frame = tk.Frame(root)
        self.difficulty_frame.pack(pady=5)

        tk.Label(self.difficulty_frame, text="Select Difficulty:", font=("Arial", 12)).pack(side="left")
        tk.Button(self.difficulty_frame, text="Easy", command=lambda: self.set_difficulty(200)).pack(side="left", padx=5)
        tk.Button(self.difficulty_frame, text="Medium", command=lambda: self.set_difficulty(150)).pack(side="left", padx=5)
        tk.Button(self.difficulty_frame, text="Hard", command=lambda: self.set_difficulty(80)).pack(side="left", padx=5)

        # Restart button
        self.restart_btn = tk.Button(root, text="Restart Game", command=self.reset_game, font=("Arial", 12))
        self.restart_btn.pack(pady=5)

        self.reset_game()

        # Key bindings
        self.root.bind("<Up>", lambda e: self.change_direction("Up"))
        self.root.bind("<Down>", lambda e: self.change_direction("Down"))
        self.root.bind("<Left>", lambda e: self.change_direction("Left"))
        self.root.bind("<Right>", lambda e: self.change_direction("Right"))

        self.running = True
        self.update()

    def set_difficulty(self, speed):
        self.speed = speed

    def reset_game(self):
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.direction = "Right"
        self.food = self.place_food()
        self.score = 0
        self.running = True
        self.update()

    def place_food(self):
        x = random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        y = random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        return (x, y)

    def change_direction(self, new_direction):
        opposites = {"Up":"Down", "Down":"Up", "Left":"Right", "Right":"Left"}
        if opposites[new_direction] != self.direction:
            self.direction = new_direction

    def move_snake(self):
        head_x, head_y = self.snake[0]
        if self.direction == "Up":
            head_y -= CELL_SIZE
        elif self.direction == "Down":
            head_y += CELL_SIZE
        elif self.direction == "Left":
            head_x -= CELL_SIZE
        elif self.direction == "Right":
            head_x += CELL_SIZE

        new_head = (head_x, head_y)

        # Check collisions
        if (head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT or new_head in self.snake):
            self.game_over()
            return

        self.snake.insert(0, new_head)

        # Check food
        if new_head == self.food:
            self.score += 1
            self.food = self.place_food()
        else:
            self.snake.pop()

    def draw(self):
        self.canvas.delete("all")

        # Draw snake
        for x, y in self.snake:
            self.canvas.create_rectangle(x, y, x+CELL_SIZE, y+CELL_SIZE, fill="green")

        # Draw food
        fx, fy = self.food
        self.canvas.create_oval(fx, fy, fx+CELL_SIZE, fy+CELL_SIZE, fill="red")

        # Draw score
        self.canvas.create_text(50, 10, text=f"Score: {self.score}", fill="white", font=("Arial", 12))

    def update(self):
        if self.running:
            self.move_snake()
            self.draw()
            self.root.after(self.speed, self.update)

    def game_over(self):
        self.running = False
        self.canvas.create_text(WIDTH//2, HEIGHT//2, text="GAME OVER", fill="white", font=("Arial", 24))
        self.canvas.create_text(WIDTH//2, HEIGHT//2+30, text=f"Final Score: {self.score}", fill="white", font=("Arial", 16))

# Run game
root = tk.Tk()
game = SnakeGame(root)
root.mainloop()
