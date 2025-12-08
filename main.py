import pygame

from game import Game

running = True

game = Game()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    game.update()

pygame.quit()

### TODO:
#make mouse aim properly with rescaled camera
