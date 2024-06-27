# A simple Pong terminal game for when I have no internet
# By Liam Dupeyron

from multiprocessing import reduction
import re
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

CRASH_SOUND = pg.mixer.Sound("/Users/liamdupeyron/Desktop/My_Pong/sound_effects/zap.mp3")
TRUMPETS = pg.mixer.Sound("/Users/liamdupeyron/Desktop/My_Pong/sound_effects/winning_trumpet.mp3")


WHITE = (225, 225, 225)
BLACK = (0, 0, 0)

PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_RADIUS = 7

SCORE_FONT = pg.font.SysFont('silom', 50)
WINNING_SCORE = 1

class Paddle:
    COLOR = WHITE
    SPEED = 6

    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
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

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y

class Ball:
    MAX_SPEED = 7
    COLOR = WHITE
    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_speed = self.MAX_SPEED
        self.y_speed = 0

    def draw(self, win):
        pg.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_speed
        self.y += self.y_speed

    def reset(self):
        pg.time.delay(500)
        self.x = self.original_x
        self.y = self.original_y
        self.x_speed *= -1
        self.y_speed = 0

def draw(win, paddles, ball, left_score, right_score):
    win.fill('black')
    # Draw the score
    left_score_text = SCORE_FONT.render(f"{left_score}", 1, WHITE)
    right_score_text = SCORE_FONT.render(f"{right_score}", 1, WHITE)
    win.blit(left_score_text, (WIDTH // 4, 20))
    win.blit(right_score_text, (WIDTH * (3/4), 20))


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
                pg.mixer.Sound.play(CRASH_SOUND)
                ball.x_speed *= -1

                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y 
                reduction_factor = (left_paddle.height / 2) / ball.MAX_SPEED
                y_speed = difference_in_y / reduction_factor
                ball.y_speed = -1 * y_speed

    # Right-paddle collision
    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                pg.mixer.Sound.play(CRASH_SOUND)
                ball.x_speed *= -1

                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y 
                reduction_factor = (right_paddle.height / 2) / ball.MAX_SPEED
                y_speed = difference_in_y / reduction_factor
                ball.y_speed = -1 *  y_speed

def main():
    run = True
    clock = pg.time.Clock()

    left_paddle = Paddle(10,(HEIGHT//2) - (PADDLE_HEIGHT//2), PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH,(HEIGHT//2) - (PADDLE_HEIGHT//2), PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WIDTH//2, HEIGHT//2, BALL_RADIUS)

    left_score = 0
    right_score = 0

    while run:
        clock.tick(FPS)
        draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score)
    
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                break
        
        keys = pg.key.get_pressed()
        hande_paddle_movement(keys, left_paddle, right_paddle)

        ball.move()
        handle_collision(ball, left_paddle, right_paddle)

        if ball.x < 0:
            right_score += 1
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            
        elif ball.x > WIDTH:
            left_score += 1
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            
        won = False
        if left_score >= WINNING_SCORE:
            won = True
            win_text = "Left Player Won!"
        elif right_score >= WINNING_SCORE:
            won = True
            win_text = "Right Player Won!"
        
        if won == True:
            text = SCORE_FONT.render(win_text, 1, WHITE)
            WIN.blit(text, (WIDTH // 2 - text.get_width()//2, HEIGHT * (1/4)))
            pg.display.update()
            pg.mixer.Sound.play(TRUMPETS)
            pg.time.delay(3100)
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0


    pg.quit()

if __name__ == '__main__':
    main()


