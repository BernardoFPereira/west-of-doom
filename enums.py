from enum import Enum

class Ability(Enum):
    """
    The base ability-bonuses and other abilities
    """

    BOD = "body"
    MND = "mind"
    GRT = "grit"
    REF = "reflex"
    CUN = "cunning"
    
    ARMOR = "armor"

    ALLEGIANCE_HOSTILE = "hostile"
    ALLEGIANCE_NEUTRAL = "neutral"
    ALLEGIANCE_FRIENDLY = "firendly"

ABILITY_REVERSE_MAP = {
    "bod": Ability.BOD,
    "mnd": Ability.MND,
    "grit": Ability.GRT,
    "reflex": Ability.REF,
    "cunning": Ability.CUN,
}

class WieldLocations(Enum):
    MAIN_HAND = "main_hand"
    OFF_HAND = "off_hand"
    TWO_HANDS = "two_handed"
    
class WearLocations(Enum):
    HEAD = "head"
    CHEST = "chest"
    HANDS = "hands"
    LEGS = "legs"
    FEET = "feet"
    BACK = "back"
    SHOULDERS = "shoulders"
    WAIST = "waist"
    BELT = "belt"

class ObjType(Enum):
    WEAPON = "weapon"
    CLOTHES = "clothing"
    SHIELD = "shield"
    HEADGEAR = "headgear"
    CONSUMABLE = "consumable"
    CONTAINER= "container"
    RELIC = "relic"
    LOOT = "loot"
    QUEST = "quest"
    GEAR = "gear"
    AMMO = "ammo"

class GearCondition(Enum):
    FLAWLESS = "flawless"
    WELL_KEPT = "well-kept"
    FINE = "fine"
    USED = "used"
    WORN = "worn"
    NEGLECTED = "neglected"
    USELESS = "useless"

class AmmoType(Enum):
    MAGNUM = "magnum"
    STANDARD = "standard"
    PLINKING = "plinking"
    SHELLS = "shells"
    ARROW = "arrow"
    BOLT = "bolt"
    
