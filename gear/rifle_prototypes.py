from enums import AmmoType, WieldLocations

BASE_RIFLE = {
  "typeclass": "typeclasses.weapons.Ranged",
  "use_equipment_slot": WieldLocations.TWO_HANDS,
}

LEVER_ACTION_45 = { 
    "prototype_parent": (BASE_RIFLE,),  
    "key": ".45 Lever-Action", 
    "desc": "A fast-firing, tube-fed rifle popular among Frontiersmen.",
    "attrs": [
        ("ammo_type", AmmoType.STANDARD),
        ("ammo_capacity", 10),
        ("weight", 3.8),
    ]
}

LONG_RANGE_44 = { 
    "prototype_parent": (BASE_RIFLE,),  
    "key": ".44 Long-Range Rifle", 
    "desc": "A heavier lever-action rifle suited for distance shooting.",
    "attrs": [
        ("ammo_type", AmmoType.MAGNUM),
        ("ammo_capacity", 8),
        ("weight", 4.1),
    ]
}

BUFFALO_50 = { 
    "prototype_parent": (BASE_RIFLE,),  
    "key": ".50 Buffalo Rifle", 
    "desc": "A high-powered hunting rifle, devastating at long range.",
    "attrs": [
        ("ammo_type", AmmoType.MAGNUM),
        ("ammo_capacity", 1),
        ("weight", 5.2),
    ]
}

VARMINT_22 = { 
    "prototype_parent": (BASE_RIFLE,),  
    "key": ".22 Varmint Rifle", 
    "desc": "A lightweight rifle suited for small game hunting.",
    "attrs": [
        ("ammo_type", AmmoType.PLINKING),
        ("ammo_capacity", 5),
        ("weight", 3.5),
    ]
}

SHARPSHOOTER_30 = { 
    "prototype_parent": (BASE_RIFLE,),  
    "key": ".30 Sharpshooter", 
    "desc": "A precision rifle favored for hunting and long-range engagements.",
    "attrs": [
        ("ammo_type", AmmoType.STANDARD),
        ("ammo_capacity", 5),
        ("weight", 4.0),
    ]
}

OUTRIDER_45 = { 
    "prototype_parent": (BASE_RIFLE,),  
    "key": ".45 Outrider", 
    "desc": "A rugged bolt-action rifle, reliable in harsh conditions.",
    "attrs": [
        ("ammo_type", AmmoType.STANDARD),
        ("ammo_capacity", 5),
        ("weight", 4.2),
    ]
}

PLAINS_50 = { 
    "prototype_parent": (BASE_RIFLE,),  
    "key": ".50 Plains Rifle", 
    "desc": "A powerful, single-shot hunting rifle used for large game.",
    "attrs": [
        ("ammo_type", AmmoType.MAGNUM),
        ("ammo_capacity", 1),
        ("weight", 4.4),
    ]
}

FRONTIER_CARBINE_38 = { 
    "prototype_parent": (BASE_RIFLE,),  
    "key": ".38 Frontier Carbine", 
    "desc": "A simple, break-open rifle with a balance of power and weight.",
    "attrs": [
        ("ammo_type", AmmoType.STANDARD),
        ("ammo_capacity", 1),
        ("weight", 3.6),
    ]
}

SETTLERS_RIFLE_45 = { 
    "prototype_parent": (BASE_RIFLE,),  
    "key": ".45 Settler's Rifle", 
    "desc": "A no-frills rifle commonly used by homesteaders and pioneers.",
    "attrs": [
        ("ammo_type", AmmoType.STANDARD),
        ("ammo_capacity", 1),
        ("weight", 3.8),
    ]
}
