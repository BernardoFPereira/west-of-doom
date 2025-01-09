"""
Room

Rooms are simple containers that has no location of their own.

"""

from evennia.objects.objects import DefaultRoom
from .objects import ObjectParent
from evennia import search_tag
from evennia.utils.utils import iter_to_str, defaultdict
from utils.utils import iter_to_multiline, capitalize_name

class Room(ObjectParent, DefaultRoom):
    """
    Rooms are like any Object, except their location is None
    (which is default). They also use basetype_setup() to
    add locks so they cannot be puppeted or picked up.
    (to change that, use at_object_creation instead)

    See examples/object.py for a list of
    properties and methods available on all Objects.
    """

    appearance_template =  """
{header}
|g{name}|n
{desc}{characters}{things}
{exits}
{footer}
    """
  
    def at_object_creation(self):
        self.db.is_dark = False
        self.db.terrain_str = ';'

    def get_display_characters(self, looker, **kwargs):
        def _filter_visible(obj_list):
            return (obj for obj in obj_list if obj != looker and obj.access(looker, "view"))

        output_list = []

        characters = _filter_visible(self.contents_get(content_type="character"))
        character_names = iter_to_multiline(
            (
                (f"{char.get_display_name(looker, **kwargs)} is {char.db.stance} here.") if not char.ndb.is_riding
                else (f"{char.get_display_name(looker, **kwargs)} is {char.db.stance} here, riding {char.ndb.mount.get_display_name()}.")
                for char in characters
            )
        )
        if character_names:
            output_list.append(character_names)
            

        animals = _filter_visible(self.contents_get(content_type="animal"))
        animal_names = iter_to_multiline(
            f"{capitalize_name(animal, looker)} is {animal.db.stance} here."
            for animal in animals
        )
        if animal_names:
            output_list.append(animal_names)

        # ridden_mounts = search_tag('ridden_mount')
        mounts = _filter_visible(self.contents_get(content_type="mount"))
        mount_names = iter_to_multiline(
                (f"{capitalize_name(mount, looker)} is {mount.db.stance} here.")
                if not mount.ndb.rider
                else(
                    # ""
                    f"{capitalize_name(mount, looker)} is {mount.db.stance} here, ridden by {(mount.ndb.rider.get_display_name(looker) if looker != mount.ndb.rider else 'you')}."
                    if mount.ndb.is_ridden and looker == mount.ndb.rider
                    else "" if mount.ndb.is_ridden and looker != mount.ndb.rider
                    else
                    (f"{capitalize_name(mount, looker)} is {mount.db.stance} here, led by {(mount.ndb.rider.get_display_name(looker) if looker != mount.ndb.rider else 'you')}.")
                )
                for mount in mounts
        )
        if mount_names:
            output_list.append(mount_names)

        return "\n" + iter_to_multiline(output_list) if output_list else ""

    def get_display_things(self, looker, **kwargs):
        def _filter_visible(obj_list):
            return (obj for obj in obj_list if obj != looker and obj.access(looker, "view"))

        # sort and handle same-named things
        things = _filter_visible(self.contents_get(content_type="object"))

        grouped_things = defaultdict(list)
        for thing in things:
            grouped_things[thing.get_display_name(looker, is_dark=True) if self.db.is_dark else thing.get_display_name(looker, **kwargs)].append(thing)

        thing_names = []
        for thingname, thinglist in sorted(grouped_things.items()):
            nthings = len(thinglist)
            thing = thinglist[0]
            singular, plural = thing.get_numbered_name(nthings, looker, key=thingname)
            thing_names.append(singular if nthings == 1 else plural)
        thing_names = iter_to_str(thing_names)
        return f"\n|wYou see:|n {thing_names}" if thing_names else ""

    def get_display_exits(self, looker, **kwargs):
        """
        Get the 'exits' component of the object description. Called by `return_appearance`.

        Args:
            looker (Object): Object doing the looking.
            **kwargs: Arbitrary data for use when overriding.
        Returns:
            str: The exits display data.

        """
        def _filter_visible(obj_list):
            return (obj for obj in obj_list if obj != looker and obj.access(looker, "view"))

        exits = _filter_visible(self.contents_get(content_type="exit"))
        exit_names = iter_to_str(
            (exi.get_display_name(looker, mode='dir') for exi in exits),
            endsep=','
            )

        return f"|wExits:|n {exit_names}" if exit_names else ""
    
    def get_display_name(self, looker=None, **kwargs):
        if looker and self.locks.check_lockstring(looker, "perm(Builder)"):
            return "{}(#{})[coords:{}]".format(self.name, self.id, (self.x, self.y, self.z))
        return self.name


    # Room Coordinate(X-Y-Z) properties
    @property
    def x(self):
        """Return the X coordinate or None."""
        x = self.tags.get(category="coordx")
        return int(x) if isinstance(x, str) else None

    @x.setter
    def x(self, x):
        """Change the X coordinate."""
        old = self.tags.get(category="coordx")
        if old is not None:
            self.tags.remove(old, category="coordx")
        if x is not None:
            self.tags.add(str(x), category="coordx")

    @property
    def y(self):
        """Return the Y coordinate or None."""
        y = self.tags.get(category="coordy")
        return int(y) if isinstance(y, str) else None
    
    @y.setter
    def y(self, y):
        """Change the Y coordinate."""
        old = self.tags.get(category="coordy")
        if old is not None:
            self.tags.remove(old, category="coordy")
        if y is not None:
            self.tags.add(str(y), category="coordy")

    @property
    def z(self):
        """Return the Z coordinate or None."""
        z = self.tags.get(category="coordz")
        return int(z) if isinstance(z, str) else None
    
    @z.setter
    def z(self, z):
        """Change the Z coordinate."""
        old = self.tags.get(category="coordz")
        if old is not None:
            self.tags.remove(old, category="coordz")
        if z is not None:
            self.tags.add(str(z), category="coordz")

    @classmethod
    def get_room_at(cls, x, y, z):
        """
        Return the room at the given location or None if not found.

        Args:
            x (int): the X coord.
            y (int): the Y coord.
            z (int): the Z coord.

        Return:
            The room at this location (Room) or None if not found.

        """
        rooms = cls.objects.filter(
            db_tags__db_key=str(x), db_tags__db_category="coordx").filter(
            db_tags__db_key=str(y), db_tags__db_category="coordy").filter(
            db_tags__db_key=str(z), db_tags__db_category="coordz")
        
        if rooms:
            return rooms[0]
        
        return None

    @classmethod
    def get_rooms_around(cls, x, y, z, distance):
        """
        Return the list of rooms around the given coordinates.

        This method returns a list of tuples (distance, room) that
        can easily be browsed.  This list is sorted by distance (the
        closest room to the specified position is always at the top
        of the list).

        Args:
            x (int): the X coord.
            y (int): the Y coord.
            z (int): the Z coord.
            distance (int): the maximum distance to the specified position.

        Returns:
            A list of tuples containing the distance to the specified
            position and the room at this distance.  Several rooms
            can be at equal distance from the position.

        """
        # Performs a quick search to only get rooms in a square
        x_r = list(reversed([str(x - i) for i in range(0, distance + 1)]))
        x_r += [str(x + i) for i in range(1, distance + 1)]
        y_r = list(reversed([str(y - i) for i in range(0, distance + 1)]))
        y_r += [str(y + i) for i in range(1, distance + 1)]
        z_r = list(reversed([str(z - i) for i in range(0, distance + 1)]))
        z_r += [str(z + i) for i in range(1, distance + 1)]
        wide = Room.objects.filter_family(
                db_tags__db_key__in=x_r, db_tags__db_category="coordx").filter(
                db_tags__db_key__in=y_r, db_tags__db_category="coordy").filter(
                db_tags__db_key__in=z_r, db_tags__db_category="coordz")

        rooms = []
        for room in wide:        
            x2 = int(room.tags.get(category="coordx"))
            y2 = int(room.tags.get(category="coordy"))
            z2 = int(room.tags.get(category="coordz"))

            distance_to_room_x = x2 - x
            distance_to_room_y = y2 - y
            distance_to_room_z = z2 - z
            
            distance_to_room = abs(distance_to_room_x) + abs(distance_to_room_y) + abs(distance_to_room_z)
            
            direction = ""

            if distance_to_room_y >= 1:
                direction += "north"
            elif distance_to_room_y <= -1:
                direction += "south"

            if distance_to_room_x >= 1:
                direction += "east"
            elif distance_to_room_x <= -1:
                direction += "west"

            if distance_to_room_z >= 1:
                direction += "up" if not direction else " and up"
            elif distance_to_room_z <= -1:
                direction += "down" if not direction else " and down"

            # if distance_to_room_x >= 1 and distance_to_room_y >= 1:
            #     direction += "up"
            # elif distance_to_room_x <= -1:
            #     direction += "down"


            rooms.append((distance_to_room,
                            room,
                            distance_to_room_x,
                            distance_to_room_y,
                            distance_to_room_z,
                            direction))

        rooms.sort(key=lambda tup: tup[0])
        return rooms
    
        ##################### CODE FOR CIRCLE SEARCH #####################
        # We now need to filter down this list to find out whether
        # these rooms are really close enough, and at what distance
        # In short: we change the square to a circle.
        # rooms = []
        # for room in wide:
        #     x2 = int(room.tags.get(category="coordx"))
        #     y2 = int(room.tags.get(category="coordy"))
        #     z2 = int(room.tags.get(category="coordz"))
        #     distance_to_room = sqrt(
        #             (x2 - x) ** 2 + (y2 - y) ** 2 + (z2 - z) ** 2)
        #     if distance_to_room <= distance:
        #         rooms.append((distance_to_room, room))
        # # Finally sort the rooms by distance
        # rooms.sort(key=lambda tup: tup[0])
        # return rooms
        ##################### CODE FOR CIRCLE SEARCH #####################

@classmethod
def turn_dark(self):
    self.db.is_dark = True

@classmethod
def turn_light(self):
    self.db.is_dark = False
    
class BuildingRoom(Room):
    def at_object_creation(self):
        self.db.is_dark = False
        self.db.terrain_str = ']'

class CityRoom(Room):
    def at_object_creation(self):
        self.db.is_dark = False
        self.db.terrain_str = '#'

class RoadRoom(Room):
    def at_object_creation(self):
        self.db.is_dark = False
        self.db.terrain_str = '+'

class FieldRoom(Room):
    def at_object_creation(self):
        self.db.is_dark = False
        self.db.terrain_str = '.'

class ForestRoom(Room):
    def at_object_creation(self):
        self.db.is_dark = False
        self.db.terrain_str = 'f'

class CavernRoom(Room):
    def at_object_creation(self):
        self.db.is_dark = True
        self.db.terrain_str = 'O'

class ShallowRoom(Room):
    def at_object_creation(self):
        self.db.is_dark = False
        self.db.terrain_str = '%'

class WaterRoom(Room):
    def at_object_creation(self):
        self.db.is_dark = False
        self.db.terrain_str = '~'
        self.db.water_flow = 0
