# A simple Pong terminal game for when I have no internet
# By Liam Dupeyron

import pygame as pg

# pygame setup
pg.init()
WIDTH, HEIGHT = 700, 500
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Pong')

def main():
    run = True

    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = FALSE

    pg.quit()

if __name__ == '__main__':
    main()


