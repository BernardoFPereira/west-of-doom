from evennia import AttributeProperty
from typeclasses.objects import Object
from enums import WieldLocations, ObjType

class Gear(Object):
    """
    Base for all equippable objects.
    
    """
    equipment_use_slot = None
    weight = AttributeProperty(0, autocreate=False)
    value = AttributeProperty(0, autocreate=False)
    obj_type = ObjType.GEAR

    def at_object_creation(self):
        pass

    def get_display_header(self, looker, **kwargs):
        pass

    def at_pre_use(self, *args, **kwargs):
        pass

class Container(Gear):
    pass
