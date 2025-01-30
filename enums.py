from enum import Enum

class Ability(Enum):
    """
    The base ability-bonuses and other abilities
    """

    BOD = "body"
    MND = "mind"

    ARMOR = "armor"

    ALLEGIANCE_HOSTILE = "hostile"
    ALLEGIANCE_NEUTRAL = "neutral"
    ALLEGIANCE_FRIENDLY = "firendly"

ABILITY_REVERSE_MAP = {
    "bod": Ability.BOD,
    "mnd": Ability.MND
}

class WieldLocations(Enum):
    RIGHT_HAND = "right_hand"
    LEFT_HAND = "left_hand"
    # TWO_HANDS = "two_handed"
    HEAD = "head"
    CHEST = "chest"
    LEGS = "legs"
    FEET = "feet"
    BACK = "back"
    RIGHT_SHOULDER = "right_shoulder"
    LEFT_SHOULDER = "left_shoulder"
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

class AmmoType(Enum):
    MAGNUM = "magnum"
    STANDARD = "standard"
    PLINKING = "plinking"
    SHELLS = "shells"
    NONE = "n/a"
    
