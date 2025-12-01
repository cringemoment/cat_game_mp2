from src.physics.box import Box, HeavyBox
from src.physics.testplatform import Platform
from src.triggers.indicator import Indicator

def ObjectFactory(object, *args, **kwargs):
    objects = {
        "box": Box,
        "heavyBox": HeavyBox,
        "platform": Platform,
        "indicator": Indicator
    }

    return objects[object.lower()](*args, **kwargs)
