import pygame

class Animation:
    def __init__(self, frames, delay):
        self.frames = []
        self.sprite = None

        for frame in frames:
            self.frames.append(pygame.image.load(f"assets/{frame}"))

        self.index = 0
        self.delay = delay
        self.timer = self.delay
        self.play_once = False

    def get_image(self):
        return self.frames[self.index]

    def next_frame(self):
        if self.play_once and self.index == len(self.frames) - 1:
            return

        self.index += 1

        if self.play_once and self.index >= len(self.frames):
            self.index = len(self.frames) - 1
        else:
            self.index %= len(self.frames)

        bottom = self.sprite.rect.bottom
        center = self.sprite.rect.centerx

        self.sprite.image = self.frames[self.index]

        self.sprite.rect = self.sprite.image.get_rect()
        self.sprite.rect.bottom = bottom
        self.sprite.rect.centerx = center

        if self.sprite.facing == -1:
            self.sprite.image = pygame.transform.flip(self.sprite.image, True, False)

    def update_timers(self, dt):
        self.timer -= dt

        if self.timer <= 0:
            self.timer = self.delay
            self.next_frame()

#if the image is called default itll automatically be set
class Sprite(pygame.sprite.Sprite):
    def __init__(self, level):
        super().__init__()
        self.level = level

        self.sprites = {}
        self.current_sprite = None

        self.facing = 1 #1 is right
        #by default all sprites should face right

    def set_sprites(self, sprites):
        if not sprites:
            return

        for sprite in sprites:
            if type(sprites[sprite]).__name__ == "Animation":
                self.sprites[sprite] = sprites[sprite]
                self.sprites[sprite].sprite = self
            else:
                self.sprites[sprite] = pygame.image.load(f"assets/{sprites[sprite]}")

        if "default" in sprites:
            self.change_image("default")

    def set_loaded_sprites(self, sprites):
        for sprite in sprites:
            self.sprites[sprite] = sprites[sprite]

        if "default" in sprites:
            self.change_image("default")

    def change_image(self, new_sprite):
        self.current_sprite = new_sprite

        bottom = self.rect.bottom if getattr(self, "rect", None) else getattr(self, "y", 0) #to make the bounding box stay on the bottom instead of the top
        center = self.rect.centerx if getattr(self, "rect", None) else getattr(self, "x", 0)

        if type(self.sprites[new_sprite]).__name__ == "Animation":
            self.image = self.sprites[new_sprite].get_image()
        else:
            self.image = self.sprites[new_sprite]

        self.rect = self.image.get_rect()

        self.rect.bottom = bottom
        self.rect.centerx = center
        self.x, self.y = self.rect.topleft

        #turning the image the right way
        if self.facing == -1:
            self.image = pygame.transform.flip(self.image, True, False)

    def get_image(self):
        if type(self.sprites[self.current_sprite]).__name__ == "Animation":
            return self.sprites[self.current_sprite].frames[self.sprites[self.current_sprite].index]
        else:
            return self.sprites[self.current_sprite]

    def set_facing(self, face):
        if face != self.facing:
            self.image = pygame.transform.flip(self.image, True, False)
            self.facing = -1 if self.facing == 1 else 1

    def update_sprites(self, dt):
        if type(self.sprites[self.current_sprite]).__name__ == "Animation":
            self.sprites[self.current_sprite].update_timers(dt)

    def play_anim(self, name, play_once = True):
        anim = self.sprites[name]

        self.current_sprite = name
        anim.play_once = play_once

        anim.index = 0
        anim.timer = anim.delay

        self.image = anim.get_image()

        if hasattr(self, "rect"):
            bottom = self.rect.bottom
            center = self.rect.centerx
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
            self.rect.centerx = center
