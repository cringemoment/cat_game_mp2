import pygame

GRAVITY = 0.5
FRICTION = 0.8
MAXX_VELO = 10
JUMP_POWER = 12

class Player(pygame.sprite.Sprite):
    def __init__(self, coords, controls):
        super().__init__()

        #handling controls
        self.jump = controls["jump"]
        self.left = controls["left"]
        self.right = controls["right"]

        #temp image
        self.image = pygame.Surface((32, 32))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(topleft=coords)

        #movement stuff
        self.x, self.y = coords
        self.velx = 0
        self.vely = 0
        self.on_ground = False
        self.accel = 1.5

    def handle_input(self):
        keys = pygame.key.get_pressed()

        # Horizontal movement
        if keys[self.left]:
            self.velx -= self.accel
        if keys[self.right]:
            self.velx += self.accel

        # Jumping
        if keys[self.jump] and self.on_ground:
            self.vely = -JUMP_POWER
            self.on_ground = False

        # Clamp horizontal velocity
        if self.velx > MAXX_VELO:
            self.velx = MAXX_VELO
        elif self.velx < -MAXX_VELO:
            self.velx = -MAXX_VELO

        # Friction
        if not keys[pygame.K_a] and not keys[pygame.K_d]:
            if self.velx > 0:
                self.velx -= FRICTION
                if self.velx < 0:
                    self.velx = 0
            elif self.velx < 0:
                self.velx += FRICTION
                if self.velx > 0:
                    self.velx = 0

    def update_pos(self, tiles):
        # --- Horizontal movement ---
        self.x += self.velx
        self.rect.x = int(self.x)

        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if self.velx > 0:  # moving right
                    self.rect.right = tile.rect.left
                elif self.velx < 0:  # moving left
                    self.rect.left = tile.rect.right
                self.velx = 0
                self.x = self.rect.x

        # --- Vertical movement ---
        self.vely += GRAVITY
        self.y += self.vely
        self.rect.y = int(self.y)
        self.on_ground = False

        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if self.vely > 0:  # falling
                    self.rect.bottom = tile.rect.top
                    self.vely = 0
                    self.on_ground = True
                elif self.vely < 0:  # jumping
                    self.rect.top = tile.rect.bottom
                    self.vely = 0
                self.y = self.rect.y

    def update(self, tiles):
        self.handle_input()
        self.update_pos(tiles)
