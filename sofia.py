# coding=utf-8
from tkinter import *

# placing ball cde
def start_place(self):
    # retrievs ball's current coordinates
    x,y, *_ = self.canvas.bbox(self.bob)
    self.canvas.move(self.bob, (GUI.CANVAS_WIDTH / 2) - x, (GUI.CANVAS_HEIGHT / 2) - y)

class GUI:
    WIDTH = 600
    HEIGHT = 600
    def __init__(self):
        self.window = Tk()
        self.canvas = Canvas(self.window, width=f"{self.WIDTH}",
                             height=f"{self.HEIGHT}",
                             background="black")
        self.canvas.pack()

        self.paddle = Paddle(self.window, self.canvas, 50, 150)

        self.window.bind('<KeyPress>', self.pressed)
        self.window.bind('<KeyRelease>', self.released)

        self.window.mainloop()

    def pressed(self, event):
        key = event.keysym
        if key == "w" or key == "Up":
            self.paddle.move(-1)
        if key == "s" or key == "Down":
            self.paddle.move(1)

    def released(self, _event):
        self.paddle.stop()


class Paddle:
    """Create paddle."""
    WIDTH = 15
    HEIGHT = 60
    SPEED = 4

    def __init__(self, window, canvas, x, y):
        """Initialize the paddle's window, canvas, x and y coordinates."""
        self.window = window
        self.canvas = canvas
        self.y_vel = 0
        self.score = 0

        self.paddle_id = canvas.create_rectangle(x, y, x + self.WIDTH,
                                              y + self.HEIGHT, fill="white")

        self.move_paddle = None

    def get_paddle_id(self):
        """Return paddle's canvas id."""
        return self.paddle_id

    def move(self, y):
        """Moves the paddle."""
        # moves the paddle in the y-axis
        self.canvas.move(self.paddle_id, 0, self.y_vel)

        # checks whether paddle is at window boundary
        if self.canvas.coords(self.paddle_id)[3] > GUI.HEIGHT:
            self.y_vel = -0.5
        elif self.canvas.coords(self.paddle_id)[1] < 0:
            self.y_vel = 0.5
        else:
            # applies speed to paddle
            self.y_vel = y * self.SPEED

        self.move_paddle = self.window.after(10, lambda: self.move(y))

    def stop(self):
        """Stops the active after function."""
        # checks if there is an after function active before canceling it
        if self.move_paddle is not None:
            self.window.after_cancel(self.move_paddle)
            self.move_paddle = None

GUI()
