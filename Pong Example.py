import tkinter as tk
import random as rand
import threading
import os

# define some constants
WIDTH = 1000
HEIGHT = 700
MARGIN = 15
VELOCITY = 15


# First, we design the Ball Object
class Ball:
    def __init__(self, canvas, width, velocity, boardwidth, boardheight):
        self.width = width
        self.boardwidth = boardwidth
        self.boardheight = boardheight
        # we center the ball on the board
        self.topx = boardwidth / 2 - width / 2
        self.topy = boardheight / 2 - width / 2
        self.velocity = velocity
        self.vx = velocity
        self.vy = velocity
        self.canvas = canvas
        self.id = self.canvas.create_rectangle(self.topx, self.topy, self.topx + self.width, self.topy + self.width,
                                               fill='white')

    # we define a method to draw the ball on the canvas
    def draw(self):
        self.canvas.coords(self.id, self.topx, self.topy, self.topx + self.width, self.topy + self.width)

    # we define a restart method for restarting the ball move
    def restart(self):
        self.topx = self.boardwidth / 2 - self.width / 2
        self.topy = self.boardheight / 2 - self.width / 2
        # we define a random direction for the ball when restarting
        self.vx = (-1, 1)[rand.random() > 0.5] * self.velocity
        self.vy = (-1, 1)[rand.random() > 0.5] * self.velocity

    # Move the ball
    # we need to pass the pong game instance and the paddles in the move method of the Ball. You can improve this by yourself later ;)
    def move(self, pong, paddleright, paddleleft):
        # if the ball touches the top or the bottom of the board, we invert direction y
        if self.topy <= 0 or (self.topy + self.width) >= self.boardheight:
            self.vy = self.vy * -1

        # if the ball touches one of both paddles, we invert direction x
        if paddleright.collideright(self) or paddleleft.collideleft(self):
            self.vx = self.vx * -1

        # if the ball touches the right or the left of the board, we update paddle points and we return True
        if (self.topx + self.width) >= self.boardwidth:
            pong.leftpoints = pong.leftpoints + 1
            return True

        if self.topx <= 0:
            pong.rightpoints = pong.rightpoints + 1
            return True

        # we update ball position
        self.topx = self.topx + self.vx
        self.topy = self.topy + self.vy

        return False


# Now, it is time to design the Paddle for our Pong Game
class Paddle:
    def __init__(self, canvas, topx, topy, width, height, boardheight):
        self.topx = topx
        self.topy = topy
        self.width = width
        self.height = height
        self.boardheight = boardheight
        self.score = 0
        self.canvas = canvas
        # draw this paddle according positions passed in parameter
        self.id = self.canvas.create_rectangle(self.topx, self.topy, self.topx + self.width, self.topy + self.height,
                                               fill='white')

    # we update coords of this paddle
    def draw(self):
        self.canvas.coords(self.id, self.topx, self.topy, self.topx + self.width, self.topy + self.height)

    # now, we need to manage down event then top event for the current paddle object
    def top(self):
        if self.topy - VELOCITY > 0:
            self.topy = self.topy - VELOCITY

    def down(self):
        if (self.topy + self.height + VELOCITY) < self.boardheight:
            self.topy = self.topy + VELOCITY

    # use both methods to collide paddle right or left. As an exercise, you can improve this to make one generic method ;)
    def collideright(self, ball):
        if (ball.topx + ball.width) >= self.topx and (
                ball.topy >= self.topy or (ball.topy + ball.width) >= self.topy) and (
                (ball.topy + ball.width) <= (self.topy + self.height) or ball.topy <= (self.topy + self.height)):
            return True

        return False

    def collideleft(self, ball):
        if ball.topx <= (self.topx + self.width) and (
                ball.topy >= self.topy or (ball.topy + ball.width) >= self.topy) and (
                (ball.topy + ball.width) <= (self.topy + self.height) or ball.topy <= (self.topy + self.height)):
            return True

        return False


# Now, we can define the Pong Game Object
class Pong:
    def __init__(self, root, width, height, margin):
        paddlewidth = width / 50
        paddleheight = height / 12
        self.leftpoints = 0
        self.lefttxt = None
        self.rightpoints = 0
        self.righttxt = None
        self.render = True  # True when we need to render the game on the canvas
        # we manage left up / down for moving the left paddle
        self.leftup = False
        self.leftdown = False
        # same for right paddle
        self.rightup = False
        self.rightdown = False
        self.width = width
        self.height = height
        self.margin = margin
        self.root = root
        self.root.title("Pong Game - SSaurel's Blog")
        self.root.geometry(str(width) + "x" + str(height))
        # we create the canvas
        self.canvas = tk.Canvas(self.root, width=width, height=height, bg='black')
        self.paddleleft = Paddle(self.canvas, margin, height / 2 - paddleheight / 2, paddlewidth, paddleheight, height)
        self.paddleright = Paddle(self.canvas, (width - margin) - paddlewidth, height / 2 - paddleheight / 2,
                                  paddlewidth, paddleheight, height)
        self.ball = Ball(self.canvas, paddlewidth, VELOCITY, width, height)
        self.canvas.pack()
        self.drawmiddlelines()
        self.drawboard()
        self.move()

    # we move draw middle lines for the board
    def drawmiddlelines(self):
        leftx = self.width / 2 - self.paddleleft.width / 2

        for y in range(0, self.height, int(self.paddleleft.height + self.margin * 2)):
            self.canvas.create_rectangle(leftx, y, leftx + self.paddleleft.width, y + self.paddleleft.height,
                                         fill='grey')

    def drawboard(self):
        try:
            # draw the paddles
            self.paddleleft.draw()
            self.paddleright.draw()

            # draw points
            self.drawpoints()

            # draw the ball
            self.ball.draw()
        except:
            # some strange exception occur here when we quit the game. We need to call explicitly exit!
            os._exit(0)

    def drawpoints(self):
        # we delete the previous score for the left paddle
        if self.lefttxt != None:
            self.canvas.delete(self.lefttxt)

        # we write the new score
        self.lefttxt = self.canvas.create_text(self.width / 2 - 50, 50, text=str(self.leftpoints), fill='grey',
                                               font=("Helvetica 35 bold"))

        # the same thing for the right paddle
        if self.righttxt != None:
            self.canvas.delete(self.righttxt)

        # we write the new score
        self.righttxt = self.canvas.create_text(self.width / 2 + 50, 50, text=str(self.rightpoints), fill='grey',
                                                font=("Helvetica 35 bold"))

    # we define the move method to update the game elements
    def move(self):
        if self.render:
            # use a timer to call this method each X milliseconds
            self.timer = threading.Timer(0.05, self.move)
            self.timer.start()

            # we manage touch events
            if self.leftup:
                self.paddleleft.top()

            if self.leftdown:
                self.paddleleft.down()

            if self.rightup:
                self.paddleright.top()

            if self.rightdown:
                self.paddleright.down()

            # True if the Ball touched one of both sides of the board
            state = self.ball.move(self, self.paddleright, self.paddleleft)

            if state:
                self.restart()  # we need to restart the ball

            self.drawboard()

    def restart(self):
        self.ball.restart()

    # Time to manage keyboards event from users
    # We need to make this special code to detect several keys used at the same time on the keyboard
    # z / s for the left paddle - o / l for the right paddle
    def keypress(self, event):
        match event.char:
            case 'z':
                self.leftup = True
            case 's':
                self.leftdown = True
            case 'o':
                self.rightup = True
            case 'l':
                self.rightdown = True

    def keyrelease(self, event):
        match event.char:
            case 'z':
                self.leftup = False
            case 's':
                self.leftdown = False
            case 'o':
                self.rightup = False
            case 'l':
                self.rightdown = False

    # last method: we define a method to kill the timer and stop the rendering of the game
    def killtimer(self):
        self.render = False
        self.timer.cancel()
        self.root.destroy()


# we can assemble the pong game elements!
root = tk.Tk()
pong = Pong(root, WIDTH, HEIGHT, MARGIN)
# we bind key press and key release events to our Pong Game Object
root.bind("<KeyPress>", pong.keypress)
root.bind("<KeyRelease>", pong.keyrelease)
# we listen to WM_DELETE_WINDOW event to kill the timer ...
root.wm_protocol("WM_DELETE_WINDOW", pong.killtimer)
root.mainloop()

# Time to try our Pong Game in Python with Tkinter

# Improvement you can make from here :
# - Make a limit points to end the game. For the moment, it is an infinite Pong Game :D
# - You can also imagine to increase the velocity of the ball each 10 points scored.
# - You can implement an AI for the second paddle
# - You can improve the design of the objects as stated in the code

# --> It is your turn to code :D