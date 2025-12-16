from src.triggers.triggerobject import Trigger
from src.renderer.camera import CameraPos, CameraTrigger
from src.triggers.testbutton import Button

def TriggerFactory(object, **kwargs):
    objects = {
        "trigger": Trigger,
        "cameratrigger": CameraTrigger,
        "camerapos": CameraPos,
        "button": Button
    }

    # print(object)
    # print(object.lower())

    if object.lower() not in objects:
        raise Exception(f"{object} not a loaded trigger")

    return objects[object.lower()](**kwargs) if object.lower() in objects else None
