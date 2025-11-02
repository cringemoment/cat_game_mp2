import pygame

class SpriteObject(pygame.sprite.Sprite): #genuinely i have no idea what to name this thing
    #its a sprite and an object but also it has multiple sprites
    #spriteobject it is

    def __init__(self, sprites):
        super().__init__()
        self.sprites = {}

        for sprite in sprites:
            self.sprites[sprite] = pygame.image.load(f"assets/sprites/{sprites[sprite]}")

    def change_image(self, new_sprite):
        print(self.sprites)
        self.image = self.sprites[new_sprite]
