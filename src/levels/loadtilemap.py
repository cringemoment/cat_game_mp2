#rn each layer is treated by its class
#class physics_objects are for physics objects
#class level is for immovable tangible stuff
#class decoration is for intangible stuff
#class positions is for positions and stuff

import pygame
import pytmx

# from src.physicsobject import PhysicsObject
from src.physics.objectfactory import ObjectFactory
from src.triggers.triggerfactory import TriggerFactory

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y, tile_size):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft = (x * tile_size, y * tile_size))
        self.x = x * tile_size
        self.y = y * tile_size
        self.left = self.x
        self.right = self.x + tile_size
        self.top = self.y
        self.bottom = self.y + tile_size

#lot of copy pasted boilerplate
class TileMap:
    def __init__(self, level, tmx_data):
        self.tmx_data = tmx_data
        self.tile_size = tmx_data.tilewidth
        self.width = tmx_data.width * self.tile_size
        self.height = tmx_data.height * self.tile_size
        self.level = level

        #separate sprite groups
        self.collision_tiles = pygame.sprite.Group()
        self.decorations = pygame.sprite.Group()
        self.physics_objects = pygame.sprite.Group()
        self.dialogue_triggers = pygame.sprite.Group()

        #positions
        self.area_triggers = []
        self.activated_objects = []

        #failsafes
        self.spawn_pos_1 = (0, 0)
        self.spawn_pos_2 = (0, 0)

        self.load_tiles()

    def load_tiles(self):
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile_image = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile_image:
                        tile = Tile(tile_image, x, y, self.tile_size)

                        #collidable only if layer class is "level"
                        if getattr(layer, "class", None) == "level":
                            self.collision_tiles.add(tile)
                        else:
                            self.decorations.add(tile)


            elif isinstance(layer, pytmx.TiledObjectGroup): #REMEMBER THAT THE CLASS OF AN OBJECT IS "type" AND NOT "class"
                if getattr(layer, "class", None) == "positions":
                    for obj in layer:
                        if obj.name == "player":
                            self.spawn_pos_1 = (obj.x, obj.y)
                        if obj.name == "player_2":
                            self.spawn_pos_2 = (obj.x, obj.y)

                        type = getattr(obj, "type", None)
                        if not type and "type" in obj.properties:
                            type = obj.properties["type"]

                        if getattr(obj, "trigger_type", None) == "activated":
                            self.activated_objects.append(TriggerFactory(type, name = obj.name, x = obj.x, y = obj.y, level = self.level, properties = obj.properties))

                        if getattr(obj, "trigger_type", None) == "trigger":
                            rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                            trigger = TriggerFactory(type, name = obj.name, rect = rect, level = self.level)

                            if self.tmx_data.get_tile_image_by_gid(obj.gid):
                                trigger.set_loaded_sprites({"default": self.tmx_data.get_tile_image_by_gid(obj.gid)})

                            self.area_triggers.append(trigger)

                elif getattr(layer, "class", None) == "physics_objects":
                    for obj in layer:
                        objclass = getattr(obj, "type", None)
                        if not objclass:
                            objclass = obj.properties["type"]

                        physics_object = ObjectFactory(objclass, self.level)

                        physics_object.set_loaded_sprites({"default": self.tmx_data.get_tile_image_by_gid(obj.gid)})
                        physics_object.name = obj.name
                        physics_object.x = obj.x
                        physics_object.y = obj.y
                        physics_object.rect.x = obj.x
                        physics_object.rect.y = obj.y
                        physics_object.change_image("default")
                        self.physics_objects.add(physics_object)

                elif getattr(layer, "class", None) == "dialogue":
                    for obj in layer:
                        rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                        self.dialogue_triggers.append(rect)

    def get_size(self):
        return self.width, self.height

def load_tilemap(window, level, path):
    tmx_data = pytmx.util_pygame.load_pygame(path)
    tilemap = TileMap(level, tmx_data)
    return tilemap
