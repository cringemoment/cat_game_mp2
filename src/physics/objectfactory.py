from src.physics.box import Box, HeavyBox

def ObjectFactory(object):
    objects = {
        "Box": Box,
        "HeavyBox": HeavyBox
    }

    return objects[object]() if object in objects else None
