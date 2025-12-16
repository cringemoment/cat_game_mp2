import pkgutil
import importlib
import inspect
import src.triggers.objects
from src.triggers.triggerobject import Trigger

objects = {"trigger": Trigger}

for _, module_name, _ in pkgutil.iter_modules(src.triggers.objects.__path__):
    module = importlib.import_module(f"src.triggers.objects.{module_name}")

    for name, obj in inspect.getmembers(module, inspect.isclass):
        if obj.__module__ == module.__name__:
            objects[name.lower()] = obj

print(objects)

def TriggerFactory(object, *args, **kwargs):
    if object.lower() not in objects:
        raise Exception(f"{object} not loaded in the trigger object factory")

    return objects[object.lower()](*args, **kwargs)
