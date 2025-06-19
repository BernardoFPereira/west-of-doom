from evennia import AttributeProperty
from typeclasses.objects import Object
from enums import WieldLocations, WearLocations, ObjType

class Gear(Object):
    """
    Base for all equippable objects.
    
    """
    equipment_use_slot = AttributeProperty(None)
    weight = AttributeProperty(0, autocreate=False)
    value = AttributeProperty(0, autocreate=False)
    
    obj_type = ObjType.GEAR

    def at_object_creation(self):
        pass

    def at_pre_move(self, destination, move_type="move", **kwargs):
        return super().at_pre_move(destination, move_type, **kwargs)
    
    def get_display_header(self, looker, **kwargs):
        return super().get_display_header(self)

    def at_pre_use(self, *args, **kwargs):
        pass

    def at_pre_drop(self, dropper, **kwargs):
        if self not in dropper.equipment.list():
            return True

        equip_type = 'wielding' if self.equipment_use_slot in WieldLocations else 'wearing' if self.equipment_use_slot in WearLocations else ""
        dropper.msg(f"You're not carrying {self.get_numbered_name(1, dropper)[0]}.")
        dropper.msg(f"However, you're {equip_type} {self.get_numbered_name(1, dropper)[0]}.")
        
        return False

class ContainerGear(Gear):
    equipment_use_slot = AttributeProperty(WearLocations.BACK)
    obj_type = ObjType.CONTAINER

