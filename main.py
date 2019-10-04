import sys

import pygame

from game import Game

pygame.init()
pygame.key.set_repeat(200, 70)

FPS = 50
WIDTH = 700
HEIGHT = 700


def terminate():
    pygame.quit()
    sys.exit()


game = Game(WIDTH, HEIGHT, FPS, ['levels/level1.txt', 'levels/level2.txt'])
game.start()

terminate()
