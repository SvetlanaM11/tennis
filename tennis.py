# подключение модулей
import tkinter
from tkinter import messagebox
import time

# окно
canvasWidth = 750
canvasHeight = 500
window = tkinter.Tk()
canvas = tkinter.Canvas(window, width=canvasWidth, height=canvasHeight, bg='dodgerblue4')
canvas.pack()
bat = canvas.create_rectangle(0, 0, 80, 10, fill='dark turquoise') # ракетка
ball = canvas.create_oval(0, 0, 30, 30, fill='deep pink') # мяч
game = True
score = 0
bounceCount = 0

# главный цикл игры
def main_loop():
    while game == True:
        move_bat()
        move_ball()
        window.update()
        time.sleep(0.02)
        if game == True:
            check_game_over()

# стрелка влево или вправо нажата
leftPressed = 0
rightPressed = 0
def key_press(event):
    global leftPressed, rightPressed
    if event.keysym == 'Left':
        leftPressed = 1
    if event.keysym == 'Right':
        rightPressed = 1

# стрелка влево или вправо отпущена
def key_off(event):
    global leftPressed, rightPressed
    if event.keysym == 'Left':
        leftPressed = 0
    if event.keysym == 'Right':
        rightPressed = 0

# движение ракетки влево-вправо
batSpeed = 10
def move_bat():
    batMove = batSpeed * rightPressed - batSpeed * leftPressed
    (batLeft, batTop, batRight, batBottom) = canvas.coords(bat)
    if (batLeft > 0 or batMove > 0) and (batRight < canvasWidth or batMove < 0):
        canvas.move(bat, batMove, 0)

# движение мяча по всему экрану
ballMoveX = 4
ballMoveY = -4
setBatTop = canvasHeight - 40
setBatBottom = canvasHeight - 30
def move_ball():
    global ballMoveX, ballMoveY, score, bounceCount, batSpeed
    (ballLeft, ballTop, ballRight, ballBottom) = canvas.coords(ball)
    if ballMoveX > 0 and ballRight > canvasWidth:
        ballMoveX = -ballMoveX
    if ballMoveX < 0 and ballLeft < 0:
        ballMoveX = -ballMoveX
    if ballMoveY < 0 and ballTop < 0:
        ballMoveY = -ballMoveY
    if ballMoveY > 0 and ballBottom > setBatTop and ballBottom < setBatBottom:
        (batLeft, batTop, batRight, batBottom) = canvas.coords(bat)
        if (ballMoveX > 0 and (ballRight + ballMoveX > batLeft and ballLeft < batRight) or ballMoveX < 0 and (ballRight > batLeft and ballLeft + ballMoveX < batRight)):
            ballMoveY = -ballMoveY
            score += 1
            bounceCount += 1
            if bounceCount == 4:
                bounceCount = 0
                batSpeed += 1
                if ballMoveX > 0:
                    ballMoveX += 1
                else:
                    ballMoveX -= 1
                ballMoveY -= 1
    canvas.move(ball, ballMoveX, ballMoveY)

# проверка или игра закончена
def check_game_over():
    (ballLeft, ballTop, ballRight, ballBottom) = canvas.coords(ball)
    if ballTop > canvasHeight:
        print(f'Your score was {score}')
        playAgain = tkinter.messagebox.askyesno(message='Do you want to play again?')
        if playAgain == True:
            game_on()
        else:
            game_off()

# конец игры
def game_off():
    global game
    game = False
    window.destroy()

# игра продолжается
def game_on():
    global score, bounceCount, batSpeed
    global leftPressed, rightPressed
    global ballMoveX, ballMoveY
    leftPressed = 0
    rightPressed = 0
    ballMoveX = 4
    ballMoveY = -4
    canvas.coords(bat, 10, setBatTop, 90, setBatBottom)
    canvas.coords(ball, 20, setBatTop - 30, 50, setBatTop)
    score = 0
    bounceCount = 0
    batSpeed = 10

# закрывает игру когда нажат х в углу окна
window.protocol('WM_DELETE_WINDOW', game_off)

# связывает окно с нажатием и отпусканием стрелок на клавиатуре
window.bind('<KeyPress>', key_press)
window.bind('<KeyRelease>', key_off)

# начало игры
game_on()

main_loop()
