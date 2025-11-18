import pygame

class Animation:
    def __init__(self, frames, delay):
        self.frames = []

        for frame in frames:
            self.frames.append(pygame.image.load(f"assets/{frame}"))

        self.index = 0
        self.delay = delay
        self.timer = self.delay

    def get_image(self):
        return self.frames[self.index]

    def next_frame(self):
        self.index = (self.index + 1) % len(self.frames)

    def update_timers(self, dt):
        self.timer -= dt

        if self.timer <= 0:
            self.timer = self.delay
            self.next_frame()

#if the image is called default itll automatically be set
class Sprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.sprites = {}

        self.facing = 1 #1 is right
        #by default all sprites should face right

    def set_sprites(self, sprites):
        if sprites:
            for sprite in sprites:
                self.sprites[sprite] = pygame.image.load(f"assets/{sprites[sprite]}")

            if "default" in sprites:
                self.change_image("default")

    def set_loaded_sprites(self, sprites):
        for sprite in sprites:
            self.sprites[sprite] = sprites[sprite]

        if "default" in sprites:
            self.change_image("default")

    def change_image(self, new_sprite):
        bottom = self.rect.bottom if getattr(self, "rect", None) else getattr(self, "y", 0) #to make the bounding box stay on the bottom instead of the top
        center = self.rect.centerx if getattr(self, "rect", None) else getattr(self, "x", 0)
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
