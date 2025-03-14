# coding=utf-8
"""This file creates a pong game inside a Tkinter window."""
import random
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
    _PADDLE_ONE_Y = CANVAS_HEIGHT / 2
    _PADDLE_TWO_X = CANVAS_HEIGHT - 50
    _PADDLE_TWO_Y = CANVAS_HEIGHT / 2

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

        self._paddle_controls = {self._paddle_one: {'UP': 'w',
                                                    'DOWN': 's'},
                                 self._paddle_two: {'UP': 'Up',
                                                    'DOWN': 'Down'}}

        self.check_collisions()
        # Begins the window
        self._window.mainloop()

    def pressed(self, event):
        """Detect when a key is pressed and move paddle."""
        # Detect which key is pressed
        key = event.keysym
        curr_paddle = self._paddle_one

        if key in self._paddle_controls[self._paddle_two].values():
            curr_paddle = self._paddle_two

        curr_controls = self._paddle_controls[curr_paddle]

        # adjust paddle speed depending on up or down key pressed
        if key == curr_controls['UP']:
            curr_paddle.set_paddle_y_vel(-Paddle.MAX_SPEED)
        if key == curr_controls['DOWN']:
            curr_paddle.set_paddle_y_vel(Paddle.MAX_SPEED)

    def released(self, event):
        """Detect when key is pressed and stop paddle."""
        # Detect which key is pressed
        key = event.keysym
        curr_paddle = self._paddle_one

        if key in self._paddle_controls[self._paddle_two].values():
            curr_paddle = self._paddle_two

        curr_paddle.stop()

    def check_collisions(self):
        """Check for collisions between ball and paddles."""
        ball_id = self._bob.get_ball_id()
        paddle_collided = [self._paddle_one.collided(ball_id),
                           self._paddle_two.collided(ball_id)]
        collided = False

        if any(paddle_collided) is True:
            collided = True

        if collided:
            self._bob.bounce()

        self._window.after(10, self.check_collisions)


class Paddle:
    """Create paddle."""

    _WIDTH = 15
    _HEIGHT = 60

    MAX_SPEED = 6

    def __init__(self, window, canvas, x, y):
        """Initialize the paddle's window, canvas, x and y coordinates."""
        self._window = window
        self._canvas = canvas
        self._y_vel = 0

        self._x = x
        self._y = y

        self._paddle_id = canvas.create_rectangle(x, y, x + self._WIDTH,
                                                  y + self._HEIGHT,
                                                  fill="white")

        self._move_paddle = None

        self.move()

    def get_paddle_id(self):
        """Return paddle's canvas id."""
        return self._paddle_id

    def set_paddle_y_vel(self, new_y_vel):
        """Set the y-velocity of the paddle."""
        self._y_vel = new_y_vel

    def move(self):
        """Move the paddles."""
        self._y += self._y_vel

        # checks if paddle hits the bottom or top of canvas, halts movements
        if self._y + self._HEIGHT > GUI.CANVAS_HEIGHT:
            self._y = GUI.CANVAS_HEIGHT - self._HEIGHT
        elif self._y < 0:
            self._y = 0

        # shifts the paddles based on the new y value
        self._canvas.coords(self._paddle_id, self._x, self._y,
                            self._x + self._WIDTH,
                            self._y + self._HEIGHT)

        self._window.after(10, self.move)

    def stop(self):
        """Stop the movement of the paddle."""
        # sets the y velocity to 0 to stop paddle from moving
        self._y_vel = 0

    def collided(self, canvas_id):
        """Check whether any object has collided with the paddle."""
        p = self._canvas.coords(self._paddle_id)
        coll = self._canvas.find_overlapping(p[0], p[1], p[2], p[3])
        # compiles a list of canvas objects overlapping with the paddles
        coll = list(coll)
        coll.remove(self._paddle_id)

        # checks if a collision has occurred and if it is with the ball
        if len(coll) != 0 and canvas_id in coll:
            self._window.after(100)
            return True
        return False


# Pedro's part.
class Ball:
    """Create and move the ball."""

    # Box dimensions
    _BOX_SIZE = 10
    _BOX_X1 = (GUI.CANVAS_WIDTH / 2) - _BOX_SIZE
    _BOX_X2 = (GUI.CANVAS_WIDTH / 2) + _BOX_SIZE
    _BOX_Y1 = (GUI.CANVAS_HEIGHT / 2) - _BOX_SIZE
    _BOX_Y2 = (GUI.CANVAS_HEIGHT / 2) + _BOX_SIZE
    # Box Speed
    _X_SPEED = 2
    _Y_SPEED = 2
    _MAX_X_SPEED = 7
    _MAX_Y_SPEED = 7
    # Score variables
    _SCORE1_X = 40
    _SCORE2_X = GUI.CANVAS_WIDTH - 35
    _SCORE_Y = 30

    def __init__(self, window, canvas):
        """Initialise ball and decide its movement."""
        # Pull from GUI class
        self._window = window
        self._canvas = canvas
        # Box movement elements
        self._x_vel = self._X_SPEED
        self._y_vel = self._Y_SPEED
        self._after_call = None
        self._bob = canvas.create_rectangle(self._BOX_X1,
                                            self._BOX_Y1,
                                            self._BOX_X2,
                                            self._BOX_Y2,
                                            fill="white")
        # Score elements
        self._paddle1_s = 0
        self._paddle2_s = 0
        # Creates the scores
        self._score_one = self._canvas.create_text(self._SCORE1_X,
                                                   self._SCORE_Y,
                                                   text=f'{self._paddle1_s}',
                                                   fill='White',
                                                   font='Monoton 26',
                                                   anchor=CENTER)
        self._score_two = self._canvas.create_text(self._SCORE2_X,
                                                   self._SCORE_Y,
                                                   text=f'{self._paddle2_s}',
                                                   fill='White',
                                                   font='Monoton 26',
                                                   anchor=CENTER)
        # call update method
        self.move_stuff()

    def get_ball_id(self):
        """Return canvas id of ball."""
        return self._bob

    def place_ball(self, new_x,  new_y):
        """Place ball at x and y."""
        # retrieves ball's current coordinates
        x, y, *_ = self._canvas.bbox(self._bob)
        self._canvas.move(self._bob, new_x - x, new_y - y)

    def restart(self):
        """Return ball to start location with a 3s delay before resuming."""
        # places ball in middle of screen
        self.place_ball((GUI.CANVAS_WIDTH / 2) - self._BOX_SIZE,
                        (GUI.CANVAS_HEIGHT / 2))

        # saves original x velocity for game resume
        original_x_vel: int = self._x_vel

        # stops movement of ball
        self._x_vel = 0
        self._y_vel = 0
        # delay to resuming the game
        self._window.after(1000,
                           lambda: self.play_after_restart(original_x_vel))

    def play_after_restart(self, x_vel):
        """Resume game."""
        # sets x-velocity to original
        self._x_vel = x_vel

    def move_stuff(self):
        """Move ball."""
        self._canvas.move(self._bob, self._x_vel, self._y_vel)

        # Boundary/collision
        if self._canvas.coords(self._bob)[2] > GUI.CANVAS_WIDTH:
            self._paddle1_s += 1
            self._x_vel = -self._x_vel
            self.restart()
            self._canvas.itemconfig(self._score_one, text=self._paddle1_s)
        if self._canvas.coords(self._bob)[0] < 0:
            self._paddle2_s += 1
            self._x_vel = -self._x_vel
            self.restart()
            self._canvas.itemconfig(self._score_two, text=self._paddle2_s)

        if (self._canvas.coords(self._bob)[3] > 600 or
                self._canvas.coords(self._bob)[1] < 0):
            self._y_vel = -self._y_vel

        # Update method
        self._after_call = self._window.after(16, self.move_stuff)

    def bounce(self):
        """Reflect ball's trajectory."""
        # boost_y adds y_vel when it decreases to 0
        boost_y = random.randrange(-self._MAX_Y_SPEED, self._Y_SPEED)
        speed_increment = 0.5

        # checks if speed within max then increments according to no signs
        if 0 < self._x_vel < self._MAX_X_SPEED:
            self._x_vel += speed_increment
        elif -self._MAX_X_SPEED < self._x_vel < 0:
            self._x_vel -= speed_increment

        # reverses trajectory
        self._x_vel = -self._x_vel

        # adds velocity to the ball when it reaches 0
        if self._y_vel == 0:
            self._y_vel += boost_y
        # varies the y-velocity of the ball
        elif self._y_vel > 0:
            self._y_vel = random.randrange(-self._y_vel, self._y_vel)
        else:
            self._y_vel = random.randrange(self._y_vel, -self._y_vel)


GUI()
