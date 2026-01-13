import pygame

class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 30
        self.height = 20

        # transition
        self.transition_time = 0
        self.transition_total = 0
        self.start_x = 0
        self.start_y = 0
        self.start_width = 0
        self.target_x = 0
        self.target_y = 0
        self.target_width = 0

    def set_level(self, level):
        self.positions = {}

        for obj in level.activated_objects:
            if type(obj).__name__ == "CameraPos":
                self.positions[obj.name] = obj

        self.x, self.y = self.positions["default"].x, self.positions["default"].y
        self.width = int(self.positions["default"].properties["screen_width"])
        self.height = int(self.positions["default"].properties.get("screen_height", self.width * 2/3))

    def transition_to(self, newx, newy, newwidth, speed):
        self.start_x = self.x
        self.start_y = self.y
        self.start_width = self.width

        self.target_x = newx
        self.target_y = newy
        self.target_width = newwidth

        self.transition_total = speed
        self.transition_time = speed

    def update_timers(self, dt):
        if self.transition_time > 0:
            self.transition_time = max(self.transition_time - dt, 0)

            t = 1 - (self.transition_time / self.transition_total)

            self.x = self.start_x + (self.target_x - self.start_x) * t
            self.y = self.start_y + (self.target_y - self.start_y) * t
            self.width = self.start_width + (self.target_width - self.start_width) * t

    def get_screen_pos(self, sprite, offset_x = 0, offset_y = 0):
        ts_x, ts_y = getattr(sprite, "ts_x", 32), getattr(sprite, "ts_y", 32)

        self.scale_factor_x = self.tile_size / ts_x
        self.scale_factor_y = self.tile_size / ts_y

        parallax = pygame.Vector2(
            getattr(sprite, "pl_x", 1.0),
            getattr(sprite, "pl_y", 1.0),
        )

        world_pos = pygame.Vector2(sprite.rect.topleft) - self.offset.elementwise() * parallax + (offset_x, offset_y)
        screen_pos = pygame.Vector2(world_pos.x * self.scale_factor_x, world_pos.y * self.scale_factor_y)

        return screen_pos

    def draw(self, surface, group):
        self.screen_rect = surface.get_rect()
        self.screen_width, screen_height = surface.get_size()
        self.offset = pygame.Vector2(self.x, self.y)

        self.tile_size = self.screen_width / self.width  # fills horizontally

        for sprite in group:
            if not getattr(sprite, "image", None):
                continue

            screen_pos = self.get_screen_pos(sprite)

            #slight optimization - check the rectangle bounds before we scale image to save time
            scaled_rect = pygame.Rect(screen_pos, (sprite.rect.width * self.scale_factor_x,  sprite.rect.height * self.scale_factor_y))

            if not self.screen_rect.colliderect(scaled_rect):
                continue

            scaled_image = pygame.transform.scale(sprite.image, scaled_rect.size)

            surface.blit(scaled_image, scaled_rect.topleft)
