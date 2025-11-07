from src.physics.box import Box

def ObjectFactory(object):
    objects = {
        "Box": Box
    }

    return objects[object]() if object in objects else None
