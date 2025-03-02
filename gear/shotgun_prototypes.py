# import random
from enums import AmmoType, ObjType#, WearLocations

BASE_SHOTGUN = {
    "typeclass": "typeclasses.weapons.Ranged",
    "obj_type": ObjType.WEAPON,
    "ammo_type": AmmoType.SHELLS,
}

SINGLE_SHOTGUN = {
    "prototype_parent": (BASE_SHOTGUN,),
    "key": "single-barreled shotgun",
    "aliases": ["shotgun", "single shotgun"],
    "ammo_capacity": 1,
    "wight": 2.7
}

DOUBLE_SHOTGUN = {
    "prototype_parent": (BASE_SHOTGUN,),
    "key": "double-barreled shotgun",
    "aliases": ["shotgun", "double shotgun"],
    "ammo_capacity": 2,
    "weight": 3.2
}


