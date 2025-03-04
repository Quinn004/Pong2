from tkinter import *

class GUI:

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

    def __init__(self):
        self.window = Tk()
        self.canvas = Canvas(self.window,
                             width=f'{self.CANVAS_WIDTH}',
                             height=f'{self.CANVAS_HEIGHT}',
                             background='Black')
        self.canvas.pack()

        self.center_line = self.canvas.create_line(
            self.LINE_X1,
            self.LINE_Y1,
            self.LINE_X2,
            self.LINE_Y2,
            fill='White',
            dash=(self.DASH_LENGTH, self.DASH_DISTANCE),
            width=self.LINE_WIDTH
            )

        self.bob = Ball(self.window, self.canvas)

        # player 1 score = Score(paddle1, x, y)
        # player 2 score = Score(paddle2, x, y)
        # paddle1 tba
        # paddle2  tba
        # ball tba

        self.window.mainloop()


    def add_score(self):
        pass


    def update(self):
        pass



#Pedro's part.
class Ball:

    BOX_X1 = (GUI.CANVAS_WIDTH / 2) - 10
    BOX_X2 = (GUI.CANVAS_WIDTH / 2) + 10
    BOX_Y1 = (GUI.CANVAS_HEIGHT / 2) - 10
    BOX_Y2 = (GUI.CANVAS_HEIGHT / 2) + 10

    X_SPEED = 5
    Y_SPEED = 5

    SCORE1_X = 20
    SCORE2_X = GUI.CANVAS_WIDTH - 20
    SCORE_Y = 15



    def __init__(self, window, canvas):
        self.window = window
        self.canvas = canvas

        self.x_vel = self.X_SPEED
        self.y_vel = self.Y_SPEED
        self.after_call = None
        self.bob = canvas.create_rectangle(self.BOX_X1,
                                           self.BOX_Y1,
                                           self.BOX_X2,
                                           self.BOX_Y2,
                                           fill="white")

        self.paddle1_s = 0
        self.paddle2_s = 0

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

        self.move_stuff()


    def move_stuff(self):
        #canvas.create_rectangle(*canvas.coords(bob))
        self.canvas.move(self.bob, self.x_vel, self.y_vel)
        #print(canvas.coords(bob))

        if self.canvas.coords(self.bob)[2] > GUI.CANVAS_WIDTH:
            self.paddle1_s += 1
            self.canvas.move(self.bob, (GUI.CANVAS_WIDTH/2), self.BOX_Y1)
            self.canvas.itemconfig(self.score_one, text=self.paddle1_s)
        if self.canvas.coords(self.bob)[0] < 0:
            self.paddle2_s += 1
            self.bob = self.canvas.create_rectangle(self.BOX_X1,
                                                    self.BOX_Y1,
                                                    self.BOX_X2,
                                                    self.BOX_Y2,
                                                    fill="white")
            self.canvas.itemconfig(self.score_two, text=self.paddle2_s)

        if self.canvas.coords(self.bob)[3] > 600 or self.canvas.coords(self.bob)[1] < 0:
          self.y_vel = -self.y_vel

        self.after_call = self.window.after(16, self.move_stuff)



GUI()
