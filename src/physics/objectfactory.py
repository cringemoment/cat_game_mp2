from src.physics.box import Box, HeavyBox
from src.physics.testplatform import Platform

def ObjectFactory(object, *args, **kwargs):
    objects = {
        "Box": Box,
        "HeavyBox": HeavyBox,
        "Platform": Platform
    }

    return objects[object](*args, **kwargs) if object in objects else None
