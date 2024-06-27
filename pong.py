# A simple Pong terminal game for when I have no internet
# By Liam Dupeyron

from sre_parse import WHITESPACE
from struct import pack
from tkinter import LEFT
from turtle import left
import pygame as pg

# pygame setup
pg.init()
WIDTH, HEIGHT = 800, 500
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Pong')

FPS = 60

WHITE = (225, 225, 225)
BLACK = (0, 0, 0)

PADDLE_WIDTH, PADDLE_HEIGHT = 10, 80
BALL_RADIUS = 7

class Paddle:
    COLOR = WHITE
    SPEED = 4

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pg.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up:
            # Move paddle upwards
            self.y -= self.SPEED
        else:
            # Move paddle downwards
            self.y += self.SPEED

class Ball:
    MAX_SPEED = 5
    COLOR = WHITE
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.x_speed = self.MAX_SPEED
        self.y_speed = 0

    def draw(self, win):
        pg.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_speed
        self.y += self.y_speed

def draw(win, paddles, ball):
    win.fill('black')

    # Draw paddles
    for paddle in paddles:
        paddle.draw(win)

    # Draw middle lines
    for i in range(10, HEIGHT, HEIGHT//20):
        if i % 2 == 0:
            pg.draw.rect(win, WHITE, (WIDTH//2, i, 5, HEIGHT//20))  

    #Draw ball
    ball.draw(win)

    pg.display.update()


def hande_paddle_movement(keys, left_paddle, right_paddle):
    # Left-paddle movement
    if keys[pg.K_w] and left_paddle.y >= 0:
        left_paddle.move()
    if keys[pg.K_s] and left_paddle.y + left_paddle.height <= HEIGHT:
        left_paddle.move(up=False)

    # Right-paddle movement
    if keys[pg.K_UP] and right_paddle.y >= 0:
        right_paddle.move()
    if keys[pg.K_DOWN] and right_paddle.y + right_paddle.height <= HEIGHT:
        right_paddle.move(up=False)
    
def handle_collision(ball, left_paddle, right_paddle):
    # Top of the screen collision
    if ball.y + ball.radius >= HEIGHT:
        ball.y_speed *= -1
    # Bottom of the screen collision
    elif ball.y - ball.radius <= 0:
        ball.y_speed *= -1

    # Left-paddle collision
    if ball.x_speed < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_speed *= -1
    # Right-paddle collision
    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_speed *= -1

def main():
    run = True
    clock = pg.time.Clock()

    left_paddle = Paddle(10,(HEIGHT//2) - (PADDLE_HEIGHT//2), PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH,(HEIGHT//2) - (PADDLE_HEIGHT//2), PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WIDTH//2, HEIGHT//2, BALL_RADIUS)

    while run:
        clock.tick(FPS)
        draw(WIN, [left_paddle, right_paddle], ball)
    
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                break
        
        keys = pg.key.get_pressed()
        hande_paddle_movement(keys, left_paddle, right_paddle)

        ball.move()
        handle_collision(ball, left_paddle, right_paddle)

    pg.quit()

if __name__ == '__main__':
    main()


