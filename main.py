import pygame

from game import Game

running = True

game = Game() #Class in game.py

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    game.update()

pygame.quit()

#TODO: fix the level 0 gap bro
