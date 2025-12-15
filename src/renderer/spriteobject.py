import pygame

class Animation:
    '''
    For displaying images on-screen

    '''
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

#if the image is called default it'll automatically be set
class Sprite(pygame.sprite.Sprite):
    """
    Objects that have image-changing abilities and functions
    Inherits from pygame.sprite.sprite
    set_sprites(sprites): loads in images from file name
    set_loaded_sprites(sprites): loads in pre-loaded sprites
    change_image(new_sprites): replaces old sprite with new sprite, y position starts at bottom
    get_image: finds the file name of the image
    set_facing(face): self.facing = current orientation, face = correct orientation. Flips image if orientation is wrong
    play_anim(name, play_once = True): Plays an animation once
    fade_in(time): Linearly fades
    """
    def __init__(self, level):
        super().__init__()
        self.level = level

        self.sprites = {}
        self.current_sprite = None
        self.transparency = 255

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

        self.image.set_alpha(self.transparency)

    def get_image(self):
        if type(self.sprites[self.current_sprite]).__name__ == "Animation":
            return self.sprites[self.current_sprite].frames[self.sprites[self.current_sprite].index]
        else:
            return self.sprites[self.current_sprite]

    def set_facing(self, face):
        if face != self.facing:
            self.image = pygame.transform.flip(self.image, True, False)
            self.facing = -1 if self.facing == 1 else 1

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

    def fade_in(self, time):
        self.fade_total = time
        self.fade_time = time
        self.fade_mode = "in"

        self.transparency = 0

    def fade_out(self, time):
        self.fade_total = time
        self.fade_time = time
        self.fade_mode = "out"

        self.transparency = 255

    def update_fade(self, dt):
        if getattr(self, "fade_mode", None) is None:
            return

        self.fade_time -= dt
        if self.fade_time < 0:
            self.fade_time = 0

        t = 1 - (self.fade_time / self.fade_total)

        if self.fade_mode == "in":
            alpha = int(t * 255)
        else:
            alpha = int((1 - t) * 255)

        alpha = max(0, min(255, alpha))
        self.transparency = alpha

        # self.image.set_alpha(self.transparency)

        if self.fade_time == 0:
            self.fade_mode = None

    def update_sprites(self, dt):
        if type(self.sprites[self.current_sprite]).__name__ == "Animation":
            self.sprites[self.current_sprite].update_timers(dt)

        self.update_fade(dt)
        self.image.set_alpha(self.transparency)

    def update(self, surface, dt):
        self.update_sprites(dt)