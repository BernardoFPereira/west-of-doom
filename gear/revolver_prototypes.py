from enums import AmmoType#, WearLocations

BASE_REVOLVER = {
    "typeclass": "typeclasses.weapons.Ranged",
    "attrs": [
        ("base_weapon_noise", 6),
    ]
}

PEACEMAKER_45 = { 
    "prototype_parent": (BASE_REVOLVER,),  
    "key": ".45 Peacemaker", 
    "desc": "The classic six-shooter, reliable and widely used.",
    "attrs": [
        ("ammo_type", AmmoType.STANDARD),
        ("ammo_capacity", 6),
        ("weight", 1.26),
    ]
}

IRONCLAD_44 = { 
    "prototype_parent": (BASE_REVOLVER,),  
    "key": ".44 Ironclad", 
    "desc": "A heavy-frame revolver that packs a stronger punch.",
    "attrs": [
        ("ammo_type", AmmoType.MAGNUM),
        ("ammo_capacity", 6),
        ("weight", 1.46),
    ]
}

NAVY_REVOLVER_36 = { 
    "prototype_parent": (BASE_REVOLVER,),  
    "key": ".36 Navy Revolver", 
    "desc": "A common sidearm for military and civilians alike.",
    "attrs": [
        ("ammo_type", AmmoType.STANDARD),
        ("ammo_capacity", 6),
        ("weight", 1.36),
    ]
}

LIGHTNING_22 = { 
    "prototype_parent": (BASE_REVOLVER,),  
    "key": ".22 Lightning", 
    "desc": "A light and fast-firing revolver, good for small game.",
    "attrs": [
        ("ammo_type", AmmoType.PLINKING),
        ("ammo_capacity", 6),
        ("weight", 1.17),
    ]
}

ARMY_MODEL_45 = { 
    "prototype_parent": (BASE_REVOLVER,),  
    "key": ".45 Army Model", 
    "desc": "Standard-issue revolver for military and lawmen.",
    "attrs": [
        ("ammo_type", AmmoType.STANDARD),
        ("ammo_capacity", 6),
        ("weight", 1.36),
    ]
}

LEMAT_CAVALRY_42 = { 
    "prototype_parent": (BASE_REVOLVER,),  
    "key": ".42 LeMat Cavalry", 
    "desc": "A hybrid revolver with an underslung shotgun barrel.",
    "attrs": [
        ("ammo_type", AmmoType.STANDARD),
        ("ammo_capacity", 9),
        ("weight", 1.99),
    ]
}

DERRINGER_45 = { 
    "prototype_parent": (BASE_REVOLVER,),  
    "key": ".45 Derringer", 
    "desc": "A tiny holdout pistol, great for concealed carry.",
    "attrs": [
        ("ammo_type", AmmoType.STANDARD),
        ("ammo_capacity", 2),
        ("weight", 0.52),
    ]
}

POCKET_REVOLVER_44 = { 
    "prototype_parent": (BASE_REVOLVER,),  
    "key": ".44 Pocket Revolver", 
    "desc": "A smaller, easier-to-carry revolver with moderate power.",
    "attrs": [
        ("ammo_type", AmmoType.STANDARD),
        ("ammo_capacity", 5),
        ("weight", 0.95),
    ]
}

