from src.physics.box import Box, HeavyBox
from src.physics.testplatform import Platform
from src.triggers.indicator import Indicator
from src.triggers.door import Door

def ObjectFactory(object, *args, **kwargs):
    objects = {
        "box": Box,
        "heavyBox": HeavyBox,
        "platform": Platform,
        "indicator": Indicator,
        "door": Door
    }

    return objects[object.lower()](*args, **kwargs)
