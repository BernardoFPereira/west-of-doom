from evennia.utils.utils import inherits_from
from enums import WieldLocations, WearLocations, Ability
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
                WieldLocations.MAIN_HAND: None,
                WieldLocations.OFF_HAND: None,
                WieldLocations.TWO_HANDS: None,
                WearLocations.HEAD: None,
                WearLocations.CHEST: None,
                WearLocations.HANDS: None,
                WearLocations.LEGS: None,
                WearLocations.FEET: None,
                WearLocations.BACK: None,
                WearLocations.SHOULDERS: None,
                WearLocations.WAIST: None,
                WearLocations.BELT: []
            }
        )

    def _save(self):
        """Save our data back to the same Attribute"""
        self.obj.attributes.add(self.save_attribute, self.slots, category="equipment")

    @property
    def max_carry_weight(self):
        """Max amount of weight, based on the BOD stat (BOD + 10) * 5.0"""
        return (getattr(self.obj, Ability.BOD.value, 6) + 10) * 5.0

    def count_carry_weight(self):
        inventory = self.obj.contents
        # slots = self.slots
        weight_usage = sum(
            getattr(obj, "weight", 0) or 0
            for obj in inventory
        )
        return weight_usage

    def validate_carry_capacity(self, obj):
        """
        Check if obj can be equipped
        
        """
        if not inherits_from(obj, Gear):
            raise EquipmentError("You're carrying to much!")

        weight = obj.weight
        max_weight = self.max_carry_weight
        current_carry_weight = self.count_carry_weight()
        return weight + current_carry_weight >= max_weight
        
    def add(self, obj):
        match obj.equipment_use_slot:
            case WieldLocations.MAIN_HAND:
                self.slots[WieldLocations.MAIN_HAND] = obj
                
            case WieldLocations.OFF_HAND:
                self.slots[WieldLocations.OFF_HAND] = obj
                
            case WearLocations.HEAD:
                self.slots[WearLocations.HEAD] = obj
                
            case WearLocations.CHEST:
                self.slots[WearLocations.CHEST] = obj
                
            case WearLocations.SHOULDERS:
                self.slots[WearLocations.SHOULDERS] = obj
                
            case WearLocations.LEGS:
                self.slots[WearLocations.LEGS] = obj
                
            case WearLocations.FEET:
                self.slots[WearLocations.FEET] = obj
                
            case WearLocations.BACK:
                self.slots[WearLocations.BACK] = obj
                
            case WearLocations.WAIST:
                self.slots[WearLocations.WAIST] = obj
                
            case WearLocations.BELT:
                self.slots[WearLocations.BELT] = obj

        self._save()

    def remove(self, obj_or_slot):
        """
        Remove specific object from equipment slot and return it to inventory.
        """

        slots = self.slots
        ret = []

        if obj_or_slot in slots.values():
            for slot, objslot in slots.items():
                if objslot is obj_or_slot:
                    slots[slot] = None
                    ret.append(objslot)

        if ret:
            self._save()

        return ret

    def move(self, obj):
        self.remove(obj)

        slots = self.slots
        use_slot = getattr(obj, "equipment_use_slot")

        to_inventory = []
        if use_slot is WieldLocations.TWO_HANDS:
            to_inventory = [slots[WieldLocations.MAIN_HAND], slots[WieldLocations.OFF_HAND]]
            slots[WieldLocations.MAIN_HAND] = slots[WieldLocations.OFF_HAND] = None
            slots[use_slot] = obj
            
        elif use_slot in (WieldLocations.MAIN_HAND, WieldLocations.OFF_HAND):
            to_inventory = [slots[WieldLocations.TWO_HANDS]]
            slots[WieldLocations.TWO_HANDS] = None
            slots[use_slot] = obj
            
        elif use_slot is None:
            to_inventory = [obj]
            
        else:
            to_inventory = [slots[use_slot]]
            slots[use_slot] = obj

        
        for to_inventory_obj in to_inventory:
            if to_inventory_obj:
                to_inventory_obj.location = self.obj
        
        self._save()

    def all(self):
        """
        Get all objects in inventory, regardless of location.
        
        """
        slots = self.slots
        lst = [
            (slots[WieldLocations.MAIN_HAND], WieldLocations.MAIN_HAND),
            (slots[WieldLocations.OFF_HAND], WieldLocations.OFF_HAND),
            (slots[WearLocations.HEAD], WearLocations.HEAD),
            (slots[WearLocations.CHEST], WearLocations.CHEST),
            (slots[WearLocations.HANDS], WearLocations.HANDS),
            (slots[WearLocations.LEGS], WearLocations.LEGS),
            (slots[WearLocations.FEET], WearLocations.FEET),
            (slots[WearLocations.BACK], WearLocations.BACK),
            (slots[WearLocations.SHOULDERS], WearLocations.SHOULDERS),
            (slots[WearLocations.WAIST], WearLocations.WAIST),
            (slots[WearLocations.BELT], WearLocations.BELT),
        ]
        return lst

    def list(self):
        slots = self.slots
        lst = [
            slots[WieldLocations.MAIN_HAND],
            slots[WieldLocations.OFF_HAND],
            slots[WearLocations.HEAD],
            slots[WearLocations.CHEST],
            slots[WearLocations.HANDS],
            slots[WearLocations.LEGS],
            slots[WearLocations.FEET],
            slots[WearLocations.BACK],
            slots[WearLocations.SHOULDERS],
            slots[WearLocations.WAIST],
            slots[WearLocations.BELT],
        ]
        return lst

    @property
    def clothing(self):
        slots = self.slots
        return sum(
            (
                getattr(slots[WearLocations.HEAD], "coverage", 1),
                getattr(slots[WearLocations.CHEST], "coverage", 1),
                getattr(slots[WearLocations.LEGS], "coverage", 1),
                getattr(slots[WearLocations.FEET], "coverage", 1),
                getattr(slots[WearLocations.BACK], "coverage", 1)
            )
        )

    @property
    def weapon(self):
        slots = self.slots
        weapon = slots[WieldLocations.TWO_HANDS]
        if not weapon:
            weapon = slots[WieldLocations.MAIN_HAND]
        if not weapon:
            return None

        return weapon
