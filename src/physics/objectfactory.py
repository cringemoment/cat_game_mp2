from src.physics.box import Box, HeavyBox
from src.physics.testplatform import Platform

def ObjectFactory(object):
    objects = {
        "Box": Box,
        "HeavyBox": HeavyBox,
        "Platform": Platform
    }

    return objects[object]() if object in objects else None
