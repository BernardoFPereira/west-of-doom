from enums import WearLocations

BASE_BELT = {
  "typeclass": "typeclasses.items.ContainerGear",
  "key": "leather belt",
  "aliases": ["belt", "leather_belt"],
  "equipment_use_slot": WearLocations.WAIST,
  "weight": 0.1
}

BASE_BANDOLIER = {
  "typeclass": "typeclasses.items.ContainerGear",
  "key": "bandolier",
  "equipment_use_slot": WearLocations.SHOULDERS,
  "weight": 0.5
}

BASE_BACKPACK = {
  "typeclass": "typeclasses.items.ContainerGear",
  "key": "backpack",
  "equipment_use_slot": WearLocations.BACK,
  "weight": 1.5
}

SHOULDER_BAG = {
  "prototype_parent": (BASE_BACKPACK,),
  "key": "shoulder bag",
  "aliases": ["shoulder_bag"],
  "equipment_use_slot": WearLocations.SHOULDERS,
  "weight": 0.7
}


