from enums import AmmoType, ObjType, WearLocations#, WieldLocations

"""
Prototypes

A prototype is a simple way to create individualized instances of a
given typeclass. It is dictionary with specific key names.

For example, you might have a Sword typeclass that implements everything a
Sword would need to do. The only difference between different individual Swords
would be their key, description and some Attributes. The Prototype system
allows to create a range of such Swords with only minor variations. Prototypes
can also inherit and combine together to form entire hierarchies (such as
giving all Sabres and all Broadswords some common properties). Note that bigger
variations, such as custom commands or functionality belong in a hierarchy of
typeclasses instead.

A prototype can either be a dictionary placed into a global variable in a
python module (a 'module-prototype') or stored in the database as a dict on a
special Script (a db-prototype). The former can be created just by adding dicts
to modules Evennia looks at for prototypes, the latter is easiest created
in-game via the `olc` command/menu.

Prototypes are read and used to create new objects with the `spawn` command
or directly via `evennia.spawn` or the full path `evennia.prototypes.spawner.spawn`.

A prototype dictionary have the following keywords:

Possible keywords are:
- `prototype_key` - the name of the prototype. This is required for db-prototypes,
  for module-prototypes, the global variable name of the dict is used instead
- `prototype_parent` - string pointing to parent prototype if any. Prototype inherits
  in a similar way as classes, with children overriding values in their parents.
- `key` - string, the main object identifier.
- `typeclass` - string, if not set, will use `settings.BASE_OBJECT_TYPECLASS`.
- `location` - this should be a valid object or #dbref.
- `home` - valid object or #dbref.
- `destination` - only valid for exits (object or #dbref).
- `permissions` - string or list of permission strings.
- `locks` - a lock-string to use for the spawned object.
- `aliases` - string or list of strings.
- `attrs` - Attributes, expressed as a list of tuples on the form `(attrname, value)`,
  `(attrname, value, category)`, or `(attrname, value, category, locks)`. If using one
   of the shorter forms, defaults are used for the rest.
- `tags` - Tags, as a list of tuples `(tag,)`, `(tag, category)` or `(tag, category, data)`.
-  Any other keywords are interpreted as Attributes with no category or lock.
   These will internally be added to `attrs` (equivalent to `(attrname, value)`.

See the `spawn` command and `evennia.prototypes.spawner.spawn` for more info.

"""

# MELEE WEAPON PROTOTYPES
CLUB = {
  "typeclass": "typeclasses.weapons.Weapon",
  "attrs": [
    ("weight", 2),
  ]
}

KNIFE = {
  "typeclass": "typeclasses.weapons.Weapon",
  "attrs": [
    ("weight", 0.5),
  ]
}

SCRAP_SWORD = {
  "typeclass": "typeclasses.weapons.Weapon",
  "attrs": [
    ("weight", 1.5),
  ]
}

# AMMO PROTOYPES
SHOTGUN_SHELL = {
  "typeclass": "typeclasses.weapons.Ammo",
  "key": "shell",
  "aliases": ["a shell", "one shell"],
  "attrs": [
    ("ammo_type", AmmoType.SHELLS),
    ("ammo_noise_bonus", 0),
    ("damage", 6),
  ],
}

PLINKING_ROUND = {
  "typeclass": "typeclasses.weapons.Ammo",
  "key": "plinking round",
  "aliases": ["plk round"],
  "attrs": [
    ("ammo_type", AmmoType.PLINKING),
    ("ammo_noise_bonus", -2),
    ("damage", 25),
  ],
}

STANDARD_ROUND = {
  "typeclass": "typeclasses.weapons.Ammo",
  "key": "standard round",
  "aliases": ["std round"],
  "attrs": [
    ("ammo_type", AmmoType.STANDARD),
    ("ammo_noise_bonus", 0),
    ("damage", 40),
  ],
}

MAGNUM_ROUND = {
  "typeclass": "typeclasses.weapons.Ammo",
  "key": "magnum round",
  "aliases": ["mgn round"],
  "attrs": [
    ("ammo_type", AmmoType.MAGNUM),
    ("damage", 55),
    ("ammo_noise_bonus", 2),
  ],
}

WOODEN_ARROW = {
  "typeclass": "typeclasses.weapons.Ammo",
  "key": "wooden arrow",
  "attrs": [
    ("ammo_type", AmmoType.ARROW),
    ("damage", 55),
    ("ammo_noise_bonus", 0),
  ]
}

BOLT = {
  "typeclass": "typeclasses.weapons.Ammo",
  "key": "bolt",
  "attrs": [
    ("ammo_type", AmmoType.BOLT),
    ("damage", 55),
    ("ammo_noise_bonus", 1),
  ]
}

# CLOTHING PROTOTYPES
BASE_SHIRT = {
  "typeclass": "typeclasses.items.Gear",
  "key": "plain shirt",
  "aliases": ["shirt", "plain_shirt"],
  "attrs": [
    ("equipment_use_slot", WearLocations.CHEST),
    ("weight", 0.2),
  ]
}
