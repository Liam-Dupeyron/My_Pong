# A simple Pong terminal game for when I have no internet
# By Liam Dupeyron

from sre_parse import WHITESPACE
from struct import pack
from tkinter import LEFT
from turtle import left
import pygame as pg

# pygame setup
pg.init()
WIDTH, HEIGHT = 700, 500
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Pong')

FPS = 60

WHITE = (225, 225, 225)
BLACK = (0, 0, 0)

PADDLE_WIDTH, PADDLE_HEIGHT = 10, 90

class Paddle:
    COLOR = WHITE
    SPEED = 5

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pg.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up:
            self.y -= self.SPEED
        else:
            self.y += self.SPEED

         
def draw(win, paddles):
    win.fill('black')

    for paddle in paddles:
        paddle.draw(win)

    pg.display.update()

def hande_paddle_movement(keys, left_paddle, right_paddle):
    if keys[pg.K_w] and left_paddle.y >= 0:
        left_paddle.move()
    if keys[pg.K_s] and left_paddle.y + left_paddle.height <= HEIGHT:
        left_paddle.move(up=False)

    if keys[pg.K_UP] and right_paddle.y >= 0:
        right_paddle.move()
    if keys[pg.K_DOWN] and right_paddle.y + right_paddle.height <= HEIGHT:
        right_paddle.move(up=False)
    


def main():
    run = True
    clock = pg.time.Clock()

    left_paddle = Paddle(10,(HEIGHT//2) - (PADDLE_HEIGHT//2), PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH,(HEIGHT//2) - (PADDLE_HEIGHT//2), PADDLE_WIDTH, PADDLE_HEIGHT)

    while run:
        clock.tick(FPS)
        draw(WIN, [left_paddle, right_paddle])
    
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                break
        
        keys = pg.key.get_pressed()
        hande_paddle_movement(keys, left_paddle, right_paddle)

    pg.quit()

if __name__ == '__main__':
    main()


