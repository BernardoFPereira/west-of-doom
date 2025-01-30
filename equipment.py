from evennia.utils.utils import inherits_from
from .enums import WieldLocations, Ability
from typeclasses.items import Gear

class EquipmentError(TypeError):
    """All types of equipment-errors"""
    pass

class EquipmentHandler:
    save_attribute = "equipment_slots"

    def __init__(self, obj):
        # Here obj is the Character we store the handler on
        self.obj = obj
        self._load()

    def _load(self):
        """Load our data from an Attribute on 'self.obj'"""

        self.slots = self.obj.attributes.get(
            self.save_attribute,
            category="equipment",
            default={
                WieldLocations.RIGHT_HAND: None,
                WieldLocations.LEFT_HAND: None,
                WieldLocations.TWO_HANDS: None,
                WieldLocations.HEAD: None,
                WieldLocations.CHEST: None,
                WieldLocations.LEGS: None,
                WieldLocations.FEET: None,
                WieldLocations.BACK: None,
                WieldLocations.RIGHT_SHOULDER: None,
                WieldLocations.LEFT_SHOULDER: None,
                WieldLocations.BELT: None
            }
        )

    def _save(self):
        """Save our data back to the same Attribute"""
        self.obj.attributes.add(self.save_attrivute, self.slots, category="equipment")

    @property
    def max_carry_weight(self):
        """Max amount of weight, based on the BOD stat (BOD + 10) * 5.0"""
        return (getattr(self.obj, Ability.BOD.value, 6) + 10) * 5.0

    def count_carry_weight(self):
        slots = self.slots
        weight_usage = sum(
            getattr(slotobj, "weight", 0) or 0
            for slot, slotobj in slots.items()
        )
        return weight_usage

    def validate_carry_capacity(self, obj):
        """
        Check if obj can be equipped
        
        """
        if not inherits_from(obj, Gear):
            raise EquipmentError(f"You can't equip {obj.key}!")

        weight = obj.weight
        max_weight = self.max_carry_weight
        current_carry_weight = self.count_carry_weight()
        return weight + current_carry_weight >= max_weight
        
