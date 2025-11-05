import pygame
import pytmx

#rn naming convention for levels is
#any tile in "deco" is ignored

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y, tile_size):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x * tile_size, y * tile_size))

#lot of copy pasted boilerplate
class TileMap:
    def __init__(self, tmx_data):
        self.tmx_data = tmx_data
        self.tile_size = tmx_data.tilewidth
        self.width = tmx_data.width * self.tile_size
        self.height = tmx_data.height * self.tile_size

        # Separate sprite groups for collisions vs visuals
        self.collision_tiles = pygame.sprite.Group()  #collision tiles
        self.decorations = pygame.sprite.Group()      #bg tiles

        self.spawn_pos = (0, 0)
        self.second_spawn_pos = (0, 0)
        self.load_tiles()

    def load_tiles(self):
        for layer in self.tmx_data.visible_layers:
            print(layer.name)
            print(dir(layer))
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile_image = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile_image:
                        tile = Tile(tile_image, x, y, self.tile_size)
                        # Collidable only if layer name is "level"
                        if layer.name.lower() == "level":
                            self.collision_tiles.add(tile)
                        else:
                            self.decorations.add(tile)

            elif isinstance(layer, pytmx.TiledObjectGroup):
                for obj in layer:
                    if obj.name == "player":
                        self.spawn_pos = (obj.x, obj.y)
                    if obj.name == "player_2":
                        self.second_spawn_pos = (obj.x, obj.y)

    def draw(self, surface):
        self.decorations.draw(surface)  # draw decorations first
        self.collision_tiles.draw(surface)  # draw level on top if desired

    def get_size(self):
        return self.width, self.height


def load_tilemap(window, path):
    tmx_data = pytmx.util_pygame.load_pygame(path)
    tilemap = TileMap(tmx_data)
    return tilemap
