# coding=utf-8
"""This file creates a pong game inside a Tkinter window."""
from tkinter import *


class GUI:
    """Create Tkinter window and initialise all instances."""

    # canvas parameters
    CANVAS_HEIGHT = 600
    CANVAS_WIDTH = 600

    # score parameters (temporary)
    TEXT_X = 50
    TEXT_Y = 50

    # center line parameters
    LINE_X1 = 300
    LINE_Y1 = 600
    LINE_X2 = 300
    LINE_Y2 = 0
    DASH_LENGTH = 7
    DASH_DISTANCE = 5
    LINE_WIDTH = 6

    # Paddle Setup
    PADDLE_ONE_X = 50
    PADDLE_ONE_Y = 150
    PADDLE_TWO_X = 550
    PADDLE_TWO_Y = 150

    def __init__(self):
        """Initialise all instances and create Tk window."""
        # Tkinter elements
        self.window = Tk()
        self.canvas = Canvas(self.window,
                             width=f'{self.CANVAS_WIDTH}',
                             height=f'{self.CANVAS_HEIGHT}',
                             background='Black')
        self.canvas.pack()
        # The dotted centre line
        self.center_line = self.canvas.create_line(
            self.LINE_X1,
            self.LINE_Y1,
            self.LINE_X2,
            self.LINE_Y2,
            fill='White',
            dash=(self.DASH_LENGTH, self.DASH_DISTANCE),
            width=self.LINE_WIDTH
            )
        # Creates the ball instance
        self.bob = Ball(self.window, self.canvas)

        # Paddle Controls
        self.window.bind('<KeyPress>', self.pressed)
        self.window.bind('<KeyRelease>', self.released)

        # Creates the paddles
        self.paddle_one = Paddle(self.window, self.canvas,
                                 self.PADDLE_ONE_X,
                                 self.PADDLE_ONE_Y)
        self.paddle_two = Paddle(self.window, self.canvas,
                                 self.PADDLE_TWO_X,
                                 self.PADDLE_TWO_Y)

        self.paddle_controls = {self.paddle_one: ['w', 's'],
                                self.paddle_two: ['Up', 'Down']}
        self.all_controls = (self.paddle_controls[self.paddle_one] +
                             self.paddle_controls[self.paddle_two])

        self.check_collisions()
        # Begins the window
        self.window.mainloop()

    def pressed(self, event):
        """Detect when a key is pressed and move paddle."""
        # Detect which key is pressed
        key = event.keysym
        curr_paddle = self.paddle_one

        if key in self.paddle_controls[self.paddle_two]:
            curr_paddle = self.paddle_two

        curr_controls = self.paddle_controls[curr_paddle]

        if key == curr_controls[0]:
            curr_paddle.y_vel = -curr_paddle.max_speed
        if key == curr_controls[1]:
            curr_paddle.y_vel = curr_paddle.max_speed

    def released(self, event):
        """Detect when key is pressed and stop paddle."""
        # Detect which key is pressed
        key = event.keysym
        curr_paddle = self.paddle_one

        if key in self.paddle_controls[self.paddle_two]:
            curr_paddle = self.paddle_two

        curr_paddle.stop()

    def check_collisions(self):
        """Check for collisions between ball and paddles."""
        paddles = [self.paddle_one.collided(), self.paddle_two.collided()]
        collided = False

        if any(paddles) is True:
            collided = True

        if collided:
            self.bob.bounce()

        self.window.after(10, self.check_collisions)


class Paddle:
    """Create paddle."""

    WIDTH = 15
    HEIGHT = 60

    MAX_SPEED = 6

    def __init__(self, window, canvas, x, y):
        """Initialize the paddle's window, canvas, x and y coordinates."""
        self.window = window
        self.canvas = canvas
        self.y_vel = 0
        self.score = 0

        self.x = x
        self.y = y

        self.paddle_id = canvas.create_rectangle(x, y, x + self.WIDTH,
                                                 y + self.HEIGHT,
                                                 fill="white")

        self.move_paddle = None

        self.max_speed = self.MAX_SPEED

        self.move()

    def get_paddle_id(self):
        """Return paddle's canvas id."""
        return self.paddle_id

    def move(self):
        """Move the paddles."""
        self.y += self.y_vel

        # checks if paddle hits the bottom or top of canvas, halts movements
        if self.y + self.HEIGHT > GUI.CANVAS_HEIGHT:
            self.y = GUI.CANVAS_HEIGHT - self.HEIGHT
        elif self.y < 0:
            self.y = 0

        # shifts the paddles based on the new y value
        self.canvas.coords(self.paddle_id, self.x, self.y, self.x + self.WIDTH,
                           self.y + self.HEIGHT)

        self.window.after(10, self.move)

    def stop(self):
        """Stop the movement of the paddle."""
        # sets the y velocity to 0 to stop paddle from moving
        self.y_vel = 0

    def collided(self):
        """Check whether any object has collided with the paddle."""
        p = self.canvas.coords(self.paddle_id)
        coll = self.canvas.find_overlapping(p[0], p[1], p[2], p[3])
        coll = list(coll)
        coll.remove(self.paddle_id)
        if len(coll) != 0:
            return True
        return False


# Pedro's part.
class Ball:
    """Create and move the ball."""

    # Box dimensions
    BOX_X1 = (GUI.CANVAS_WIDTH / 2) - 10
    BOX_X2 = (GUI.CANVAS_WIDTH / 2) + 10
    BOX_Y1 = (GUI.CANVAS_HEIGHT / 2) - 10
    BOX_Y2 = (GUI.CANVAS_HEIGHT / 2) + 10
    # Box Speed
    X_SPEED = 2
    Y_SPEED = 2
    # Score variables
    SCORE1_X = 20
    SCORE2_X = GUI.CANVAS_WIDTH - 20
    SCORE_Y = 15

    def __init__(self, window, canvas):
        """Initialise ball and decide its movement."""
        # Pull from GUI class
        self.window = window
        self.canvas = canvas
        # Box movement elements
        self.x_vel = self.X_SPEED
        self.y_vel = self.Y_SPEED
        self.after_call = None
        self.bob = canvas.create_rectangle(self.BOX_X1,
                                           self.BOX_Y1,
                                           self.BOX_X2,
                                           self.BOX_Y2,
                                           fill="white")
        # Score elements
        self.paddle1_s = 0
        self.paddle2_s = 0
        # Creates the scores
        self.score_one = self.canvas.create_text(self.SCORE1_X,
                                                 self.SCORE_Y,
                                                 text=f'{self.paddle1_s}',
                                                 fill='White',
                                                 anchor=CENTER)
        self.score_two = self.canvas.create_text(self.SCORE2_X,
                                                 self.SCORE_Y,
                                                 text=f'{self.paddle2_s}',
                                                 fill='White',
                                                 anchor=CENTER)
        # call update method
        self.move_stuff()

    def start_place(self):
        """Return ball to original location."""
        # retrieves ball's current coordinates
        x, y, *_ = self.canvas.bbox(self.bob)
        self.canvas.move(self.bob, (GUI.CANVAS_WIDTH / 2) - x,
                         (GUI.CANVAS_HEIGHT / 2) - y)

    def move_stuff(self):
        """Move ball."""
        self.canvas.move(self.bob, self.x_vel, self.y_vel)

        # Boundary/collision
        if self.canvas.coords(self.bob)[2] > GUI.CANVAS_WIDTH:
            self.paddle1_s += 1
            self.x_vel = -self.x_vel
            self.start_place()
            self.canvas.itemconfig(self.score_one, text=self.paddle1_s)
        if self.canvas.coords(self.bob)[0] < 0:
            self.paddle2_s += 1
            self.x_vel = -self.x_vel
            self.start_place()
            self.canvas.itemconfig(self.score_two, text=self.paddle2_s)

        if (self.canvas.coords(self.bob)[3] > 600 or
                self.canvas.coords(self.bob)[1] < 0):
            self.y_vel = -self.y_vel

        # Update method
        self.after_call = self.window.after(16, self.move_stuff)

    def bounce(self):
        """Reflect ball's trajectory."""
        self.x_vel = -self.x_vel


GUI()
