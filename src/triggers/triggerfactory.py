from src.triggers.triggerobject import Trigger
from src.renderer.camera import CameraPos, CameraTrigger
from src.triggers.testbutton import Button

def TriggerFactory(object, **kwargs):
    objects = {
        "Trigger": Trigger,
        "CameraTrigger": CameraTrigger,
        "CameraPos": CameraPos,
        "Button": Button
    }

    return objects[object](**kwargs) if object in objects else None
