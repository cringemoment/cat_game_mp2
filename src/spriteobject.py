import pygame

class Sprite(pygame.sprite.Sprite):

    def __init__(self, sprites):
        super().__init__()
        self.sprites = {}

        for sprite in sprites:
            self.sprites[sprite] = pygame.image.load(f"assets/sprites/{sprites[sprite]}")

    def change_image(self, new_sprite):
        self.image = self.sprites[new_sprite]
