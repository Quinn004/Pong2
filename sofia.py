# coding=utf-8
"""This file creates a pong game inside a Tkinter window."""
from tkinter import *


class GUI:
    """Create Tkinter window and initialise all instances."""

    # canvas parameters
    CANVAS_HEIGHT = 600
    CANVAS_WIDTH = 600

    # center line parameters
    _LINE_X1 = 300
    _LINE_Y1 = 600
    _LINE_X2 = 300
    _LINE_Y2 = 0
    _DASH_LENGTH = 7
    _DASH_DISTANCE = 5
    _LINE_WIDTH = 6

    # Paddle Setup
    _PADDLE_ONE_X = 50
    _PADDLE_ONE_Y = 150
    _PADDLE_TWO_X = 550
    _PADDLE_TWO_Y = 150

    def __init__(self):
        """Initialise all instances and create Tk window."""
        # Tkinter elements
        self._window = Tk()
        self._canvas = Canvas(self._window,
                              width=f'{self.CANVAS_WIDTH}',
                              height=f'{self.CANVAS_HEIGHT}',
                              background='Black')
        self._canvas.pack()
        # The dotted centre line
        self._center_line = self._canvas.create_line(
            self._LINE_X1,
            self._LINE_Y1,
            self._LINE_X2,
            self._LINE_Y2,
            fill='White',
            dash=(self._DASH_LENGTH, self._DASH_DISTANCE),
            width=self._LINE_WIDTH
            )
        # Creates the ball instance
        self._bob = Ball(self._window, self._canvas)

        # Paddle Controls
        self._window.bind('<KeyPress>', self.pressed)
        self._window.bind('<KeyRelease>', self.released)

        # Creates the paddles
        self._paddle_one = Paddle(self._window, self._canvas,
                                  self._PADDLE_ONE_X,
                                  self._PADDLE_ONE_Y)
        self._paddle_two = Paddle(self._window, self._canvas,
                                  self._PADDLE_TWO_X,
                                  self._PADDLE_TWO_Y)

        self._paddle_controls = {self._paddle_one: ['w', 's'],
                                 self._paddle_two: ['Up', 'Down']}

        self.check_collisions()
        # Begins the window
        self._window.mainloop()

    def pressed(self, event):
        """Detect when a key is pressed and move paddle."""
        # Detect which key is pressed
        key = event.keysym
        curr_paddle = self._paddle_one

        if key in self._paddle_controls[self._paddle_two]:
            curr_paddle = self._paddle_two

        curr_controls = self._paddle_controls[curr_paddle]

        if key == curr_controls[0]:
            curr_paddle.set_paddle_y_vel(-Paddle.MAX_SPEED)
        if key == curr_controls[1]:
            curr_paddle.set_paddle_y_vel(Paddle.MAX_SPEED)

    def released(self, event):
        """Detect when key is pressed and stop paddle."""
        # Detect which key is pressed
        key = event.keysym
        curr_paddle = self._paddle_one

        if key in self._paddle_controls[self._paddle_two]:
            curr_paddle = self._paddle_two

        curr_paddle.stop()

    def check_collisions(self):
        """Check for collisions between ball and paddles."""
        paddles = [self._paddle_one.collided(), self._paddle_two.collided()]
        collided = False

        if any(paddles) is True:
            collided = True

        if collided:
            self._bob.bounce()

        self._window.after(1, self.check_collisions)


class Paddle:
    """Create paddle."""

    WIDTH = 15
    HEIGHT = 60

    MAX_SPEED = 6

    def __init__(self, window, canvas, x, y):
        """Initialize the paddle's window, canvas, x and y coordinates."""
        self._window = window
        self._canvas = canvas
        self._y_vel = 0

        self._x = x
        self._y = y

        self._paddle_id = canvas.create_rectangle(x, y, x + self.WIDTH,
                                                  y + self.HEIGHT,
                                                  fill="white")

        self._move_paddle = None

        self.move()

    def get_paddle_id(self):
        """Return paddle's canvas id."""
        return self._paddle_id

    def set_paddle_y_vel(self, new_y_vel):
        self._y_vel = new_y_vel

    def move(self):
        """Move the paddles."""
        self._y += self._y_vel

        # checks if paddle hits the bottom or top of canvas, halts movements
        if self._y + self.HEIGHT > GUI.CANVAS_HEIGHT:
            self._y = GUI.CANVAS_HEIGHT - self.HEIGHT
        elif self._y < 0:
            self._y = 0

        # shifts the paddles based on the new y value
        self._canvas.coords(self._paddle_id, self._x, self._y, self._x + self.WIDTH,
                            self._y + self.HEIGHT)

        self._window.after(10, self.move)

    def stop(self):
        """Stop the movement of the paddle."""
        # sets the y velocity to 0 to stop paddle from moving
        self._y_vel = 0

    def collided(self):
        """Check whether any object has collided with the paddle."""
        p = self._canvas.coords(self._paddle_id)
        coll = self._canvas.find_overlapping(p[0], p[1], p[2], p[3])
        # compiles a list of overlapping canvas objects
        coll = list(coll)
        coll.remove(self._paddle_id)
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
        self._window = window
        self._canvas = canvas
        # Box movement elements
        self._x_vel = self.X_SPEED
        self._y_vel = self.Y_SPEED
        self._after_call = None
        self._bob = canvas.create_rectangle(self.BOX_X1,
                                            self.BOX_Y1,
                                            self.BOX_X2,
                                            self.BOX_Y2,
                                            fill="white")
        # Score elements
        self._paddle1_s = 0
        self._paddle2_s = 0
        # Creates the scores
        self._score_one = self._canvas.create_text(self.SCORE1_X,
                                                   self.SCORE_Y,
                                                   text=f'{self._paddle1_s}',
                                                   fill='White',
                                                   anchor=CENTER)
        self._score_two = self._canvas.create_text(self.SCORE2_X,
                                                   self.SCORE_Y,
                                                   text=f'{self._paddle2_s}',
                                                   fill='White',
                                                   anchor=CENTER)
        # call update method
        self.move_stuff()

    def start_place(self):
        """Return ball to original location."""
        # retrieves ball's current coordinates
        x, y, *_ = self._canvas.bbox(self._bob)
        self._canvas.move(self._bob, (GUI.CANVAS_WIDTH / 2) - x,
                          (GUI.CANVAS_HEIGHT / 2) - y)

    def move_stuff(self):
        """Move ball."""
        self._canvas.move(self._bob, self._x_vel, self._y_vel)

        # Boundary/collision
        if self._canvas.coords(self._bob)[2] > GUI.CANVAS_WIDTH:
            self._paddle1_s += 1
            self._x_vel = -self._x_vel
            self.start_place()
            self._canvas.itemconfig(self._score_one, text=self._paddle1_s)
        if self._canvas.coords(self._bob)[0] < 0:
            self._paddle2_s += 1
            self._x_vel = -self._x_vel
            self.start_place()
            self._canvas.itemconfig(self._score_two, text=self._paddle2_s)

        if (self._canvas.coords(self._bob)[3] > 600 or
                self._canvas.coords(self._bob)[1] < 0):
            self._y_vel = -self._y_vel

        # Update method
        self._after_call = self._window.after(16, self.move_stuff)

    def bounce(self):
        """Reflect ball's trajectory."""
        if 0 < self._x_vel < 6:
            self._x_vel += 0.005
        elif -6 < self._x_vel < 0:
            self._x_vel -= 0.005

        self._x_vel = -self._x_vel
        self._y_vel = -self._y_vel

GUI()
