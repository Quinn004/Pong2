
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


class Score:


    def __int__(self, paddle, canvas, x, y):
        self.paddle = paddle
        self.canvas = canvas
        self.text_x = x
        self.text_y = y

        self.score_label = self.canvas.create_text(self.text_x,
                                                   self.text_y,
                                                   text='Score: ',
                                                   fill='White',
                                                   anchor=CENTER)

GUI()
