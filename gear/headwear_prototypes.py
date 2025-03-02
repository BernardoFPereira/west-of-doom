from enums import ObjType, WearLocations

BASE_HAT = {
  "typeclass": "typeclasses.items.Gear",
  "key": "hat",
  "attrs": [
      ("obj_type", ObjType.HEADGEAR),
      ("equipment_use_slot", WearLocations.HEAD),
      ("weight", 0.2),
  ]
}

COWBOY_HAT = {
    "prototype_parent": (BASE_HAT,),
    "key": "cowboy hat",
    "aliases": ["cowboy"],
    "weight": 0.30,
    "desc": "The iconic wide-brimmed hat made of felt or straw that offers sun and rain protection.",
}

GAMBLER_HAT = {
    "prototype_parent": (BASE_HAT,),
    "key": "gambler hat",
    "aliases": ["gambler"],
    "weight": 0.25,
    "desc": "A slimmer, refined hat favored by card players and those seeking a touch of elegance on the frontier.",
}

PANAMA_HAT = {
    "prototype_parent": (BASE_HAT,),
    "key": "panama hat",
    "aliases": ["panama"],
    "weight": 0.20,
    "desc": "A lightweight straw hat ideal for warm climates, prized for its breathability and casual, relaxed style.",
}

BOWLER_HAT = {
    "prototype_parent": (BASE_HAT,),
    "key": "bowler hat",
    "aliases": ["bowler"],
    "weight": 0.30,
    "desc": "A rounded, stiff hat with a neat appearance, often worn by respectable city folk or lawmen in frontier towns for a polished, formal look.",
}

FEDORA = {
    "prototype_parent": (BASE_HAT,),
    "key": "fedora",
    "aliases": ["fedora"],
    "weight": 0.30,
    "desc": "A stylish hat with a pinched crown and narrower brim that offers a versatile, refined look—suitable for those seeking urban flair on the frontier.",
}

STRAW_HAT = {
    "prototype_parent": (BASE_HAT,),
    "key": "casual straw hat",
    "aliases": ["straw"],
    "weight": 0.25,
    "desc": "A simple, utilitarian hat worn by laborers for everyday comfort and light sun protection.",
}

WIDE_HAT = {
    "prototype_parent": (BASE_HAT,),
    "key": "wide-brimmed leather hat",
    "aliases": ["wide-brimmed"],
    "weight": 0.40,
    "desc": "A heavier, durable hat made of leather, designed to offer extra protection in harsh weather conditions.",
}

BOLERO_HAT = {
    "prototype_parent": (BASE_HAT,),
    "key": "bolero hat",
    "aliases": ["bolero"],
    "weight": 0.15,
    "desc": "A small, decorative hat that adds a unique, fashionable touch without the bulk of larger styles.",
}

TOP_HAT = {
    "prototype_parent": (BASE_HAT,),
    "key": "top hat",
    "aliases": ["top"],
    "weight": 0.45,
    "desc": "A tall, formal hat often associated with dignitaries and well-to-do citizens, lending an air of sophistication even on the frontier.",
}

SOMBRERO = {
    "prototype_parent": (BASE_HAT,),
    "key": "sombrero",
    "aliases": ["sombrero"],
    "weight": 0.35,
    "desc": "A wide-brimmed hat with a high crown, providing excellent sun protection in arid climates, common in Southwestern regions.",
}

TRAPPER_HAT = {
    "prototype_parent": (BASE_HAT,),
    "key": "trapper hat",
    "aliases": ["trapper"],
    "weight": 0.40,
    "desc": "A fur-lined hat ideal for cold weather, popular among trappers and frontiersmen braving harsher climates.",
}

CAMP_HAT = {
    "prototype_parent": (BASE_HAT,),
    "key": "camp hat",
    "aliases": ["camp"],
    "weight": 0.25,
    "desc": "A lightweight, broad-brimmed hat used by laborers or campers for practical, no-frills sun protection in everyday work.",
}

BANDANA = {
    "prototype_parent": (BASE_HAT,),
    "key": "bandana",
    "aliases": ["bandana"],
    "weight": 0.07,
    "desc": "A lightweight, square piece of cloth often tied around the head for dust protection or to keep sweat at bay.",
}

KERCHIEF = {
    "prototype_parent": (BASE_HAT,),
    "key": "kerchief",
    "aliases": ["kerchief"],
    "weight": 0.07,
    "desc": "Similar to a bandana but usually more decorative or patterned; worn around the head or neck for practical or modest purposes.",
}

HEADBAND = {
    "prototype_parent": (BASE_HAT,),
    "key": "headband",
    "aliases": ["headband"],
    "weight": 0.03,
    "desc": "A narrow strip of cloth or leather used to keep hair and sweat out of the eyes; extremely lightweight and practical.",
}

COONSKIN_CAP = {
    "prototype_parent": (BASE_HAT,),
    "key": "coonskin cap",
    "aliases": ["coonskin"],
    "weight": 0.20,
    "desc": "A casual, rustic cap made from raccoon fur, offering a rugged, frontier look.",
}

BALACLAVA = {
    "prototype_parent": (BASE_HAT,),
    "key": "balaclava",
    "aliases": ["balaclava"],
    "weight": 0.15,
    "desc": "A close-fitting head covering that provides protection against wind and cold, useful during harsh weather or long rides.",
}

TURBAN = {
    "prototype_parent": (BASE_HAT,),
    "key": "turban",
    "aliases": ["turban"],
    "weight": 0.25,
    "desc": "A long strip of cloth wrapped around the head; in the Old West, often worn by desert travelers or those influenced by multicultural traditions.",
}

BONNET = {
    "prototype_parent": (BASE_HAT,),
    "key": "ladies' bonnet",
    "aliases": ["bonnet"],
    "weight": 0.15,
    "desc": "A decorative, often lace-trimmed bonnet typically worn by women, offering modest sun protection while adding an elegant, refined touch.",
}

FLAT_CAP = {
    "prototype_parent": (BASE_HAT,),
    "key": "flat cap",
    "aliases": ["flat"],
    "weight": 0.15,
    "desc": "A low-profile, rounded cap with a small brim, usually made of tweed or cotton; offers a casual, understated look suitable for both urban and working-class styles.",
}

