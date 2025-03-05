import sys
from tkinter import *


class GUI:
    """"""

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

        self.paddle_one = Paddle(self.window, self.canvas, self.PADDLE_ONE_X,
                            self.PADDLE_ONE_Y)
        self.paddle_two = Paddle(self.window, self.canvas, self.PADDLE_TWO_X,
                            self.PADDLE_TWO_Y)

        # Begins the window
        self.window.mainloop()

    def pressed(self, event):
        key = event.keysym
        if key == "w":
            self.paddle_one.move(-1)
        if key == "Up":
            self.paddle_two.move(-1)
        if key == "s" :
            self.paddle_one.move(1)
        if key == "Down":
            self.paddle_two.move(1)

    def released(self, _event):
        self.paddle_one.stop()


class Paddle:
    """Create paddle."""
    WIDTH = 15
    HEIGHT = 60

    def __init__(self, window, canvas, x, y):
        """Initialize the paddle's window, canvas, x and y coordinates."""
        self.window = window
        self.canvas = canvas
        self.y_vel = 0
        self.score = 0

        self.paddle_id = canvas.create_rectangle(x, y, x + self.WIDTH,
                                              y + self.HEIGHT, fill="white")

        self.move_paddle = None

        self.max_speed = 10
        if sys.platform == "darwin":
            self.max_speed = 6

    def get_paddle_id(self):
        """Return paddle's canvas id."""
        return self.paddle_id

    def move(self, y):
        """Moves the paddle."""
        # moves the paddle in the y-axis
        self.canvas.move(self.paddle_id, 0, self.y_vel)

        # checks whether paddle is at window boundary
        if self.canvas.coords(self.paddle_id)[3] > GUI.CANVAS_HEIGHT:
            self.y_vel = -0.5
        elif self.canvas.coords(self.paddle_id)[1] < 0:
            self.y_vel = 0.5
        else:
            # applies speed to paddle
            self.y_vel = y * self.max_speed

        if self.move_paddle is not None and sys.platform != "darwin":
            self.move_paddle = self.window.after(10, lambda: self.move(y))
        else:
            self.move_paddle = self.window.after(10, lambda: self.move(y))

    def stop(self):
        """Stops the active after function."""
        # checks if there is an after function active before canceling it
        if self.move_paddle is not None:
            self.window.after_cancel(self.move_paddle)
            self.move_paddle = None


#Pedro's part.
class Ball:

    # Box dimensions
    BOX_X1 = (GUI.CANVAS_WIDTH / 2) - 10
    BOX_X2 = (GUI.CANVAS_WIDTH / 2) + 10
    BOX_Y1 = (GUI.CANVAS_HEIGHT / 2) - 10
    BOX_Y2 = (GUI.CANVAS_HEIGHT / 2) + 10
    # Box Speed
    X_SPEED = 5
    Y_SPEED = 5
    # Score variables
    SCORE1_X = 20
    SCORE2_X = GUI.CANVAS_WIDTH - 20
    SCORE_Y = 15



    def __init__(self, window, canvas):
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
        # retrieves ball's current coordinates
        x, y, *_ = self.canvas.bbox(self.bob)
        self.canvas.move(self.bob, (GUI.CANVAS_WIDTH / 2) - x,
                         (GUI.CANVAS_HEIGHT / 2) - y)

    def move_stuff(self):
        #canvas.create_rectangle(*canvas.coords(bob))
        self.canvas.move(self.bob, self.x_vel, self.y_vel)
        #print(canvas.coords(bob))


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

        if self.canvas.coords(self.bob)[3] > 600 or self.canvas.coords(self.bob)[1] < 0:
          self.y_vel = -self.y_vel

        # Update method
        self.after_call = self.window.after(16, self.move_stuff)



GUI()
