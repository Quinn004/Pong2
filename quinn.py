from tkinter import *

class GUI:

    CANVAS_HEIGHT = 600
    CANVAS_WIDTH = 600
    TEXT_X = 50
    TEXT_Y = 50

    RECT_X1 = 290
    RECT_Y1 = 600
    RECT_X2 = 310
    RECT_Y2 = 0


    def __init__(self):
        self.window = Tk()
        self.canvas = Canvas(self.window,
                             width=f'{self.CANVAS_WIDTH}',
                             height=f'{self.CANVAS_HEIGHT}',
                             background='Black')
        self.canvas.pack()

        self.center_line = self.canvas.create_rectangle(self.RECT_X1,
                                                        self.RECT_Y1,
                                                        self.RECT_X2,
                                                        self.RECT_Y2,
                                                        fill='White'
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

#Pedro's part.
class Ball:

    BOX_X1 = (GUI.CANVAS_WIDTH / 2) - 10
    BOX_X2 = (GUI.CANVAS_WIDTH / 2) + 10
    BOX_Y1 = (GUI.CANVAS_HEIGHT / 2) - 10
    BOX_Y2 = (GUI.CANVAS_HEIGHT / 2) + 10

    def __init__(self, window, canvas):
        self.window = window
        self.canvas = canvas

        self.start_text = canvas.create_text(GUI.CANVAS_WIDTH / 2, 300, text="Click to start",
                                        fill="white",
                                        font="Times 26 italic",
                                        anchor=CENTER)

        self.x_vel = 10
        self.y_vel = 10
        self.after_call = None
        self.bob = canvas.create_rectangle(self.BOX_X1, self.BOX_Y1, self.BOX_X2, self.BOX_Y2, fill="white")
        self.canvas.bind("<Button-1>", self.mouse_clicked)
        # move_stuff()


    def stop(self):

        self.window.after_cancel(self.after_call)
        self.canvas.delete(self.start_text)

    def mouse_clicked(self, event):
        #print(event)
        #canvas.create_rectangle(event.x-50, event.y+50, event.x+50, event.y+50, fill=f"#{random.randint(0, 0xFFFFFF):06x}")

        if self.start_text in self.canvas.find_overlapping(event.x, event.y, event.x, event.y):
            self.move_stuff()


    def move_stuff(self):
        #canvas.create_rectangle(*canvas.coords(bob))
        self.canvas.move(self.bob, self.x_vel, self.y_vel)
        #print(canvas.coords(bob))

        if self.canvas.coords(self.bob)[2] > GUI.CANVAS_WIDTH or self.canvas.coords(self.bob)[0] < 0:
            self.x_vel = -self.x_vel
        if self.canvas.coords(self.bob)[3] > 600 or self.canvas.coords(self.bob)[1] < 0:
            self.y_vel = -self.y_vel

        self.after_call = self.window.after(16, self.move_stuff)



GUI()
