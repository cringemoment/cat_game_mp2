import pygame

class Sprite(pygame.sprite.Sprite):
    def __init__(self, sprites):
        super().__init__()

        self.sprites = {}
        self.facing = 1 #1 is right
        #by default all sprites should face right

        for sprite in sprites:
            self.sprites[sprite] = pygame.image.load(f"assets/sprites/{sprites[sprite]}")

    def change_image(self, new_sprite):
        bottom = self.rect.bottom if getattr(self, "rect", None) else self.y #to make the bounding box stay on the bottom instead of the top
        center = self.rect.centerx if getattr(self, "rect", None) else self.x
        self.image = self.sprites[new_sprite]
        self.rect = self.image.get_rect()
        self.rect.bottom = bottom
        self.rect.centerx = center
        self.x, self.y = self.rect.topleft

        #turning the image the right way
        if self.facing == -1:
            self.image = pygame.transform.flip(self.image, True, False)

    def set_facing(self, face):
        if face != self.facing:
            self.image = pygame.transform.flip(self.image, True, False)
            self.facing = -1 if self.facing == 1 else 1
