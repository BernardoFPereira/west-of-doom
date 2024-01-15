from typeclasses.exits import Exit

from evennia.utils.funcparser import FuncParser
from evennia.utils.funcparser import funcparser_callable_an

from evennia.utils.utils import make_iter
from utils.utils import iter_to_multiline, capitalize_name

parser = FuncParser({"an":funcparser_callable_an})

class Door(Exit):
    
#     appearance_template =  """
# {header}
# |g{name}|n
# {desc}{characters}{things}
# {exits}
# {footer}
#     """

    def at_object_creation(self):
        self.tags.add('door')

        self.db.desc = "This is a Door object."
        self.db.door_name = 'door'
        
        self.db.is_open = False
        self.db.return_exit = None

        self.db.desc_state = f"The {self.db.door_name} is closed."
    
    def set_door_name(self, name):
        """
        Sets identical names on both both sides of the door.

        Args:
            set_name(str) : the name to be set on both sides
            of the door.
        """
        self.db.door_name = name
        self.db.return_exit.db.door_name = name

    def set_state(self, state_description):
        """
        Sets identical state descriptions on both sides of the door.

        Args:
            set_state (str): A state description.

        """
        self.db.desc_state = state_description
        self.db.return_exit.db.desc_state = state_description

    def connect_other_side(self, named=True, same_desc=True):
        """
        Links-up doors based on cardinal directions.
        It detects 'our' direction and looks up the opposite
        on the other side.

        Args:
            connect_other_side (bool[optional], bool[optional]):
            if named is True, transfer door_name to the other side of
            the door as a name and alias.
            if same_desc is True, transfer description to the other
            side of the door.
        """
        
        direction_dict = {
            "n": ("north", "s"),
            "e": ("east", "w"),
            "s": ("south", "n"),
            "w": ("west", "e"),
            "u": ("up", "d"),
            "d": ("down", "u"),
            "i": ("in", "o"),
            "o": ("out", "i"),
        }
        
        # door_direction = self.aliases.get()[0]
        door_direction = self.key[0]
        door_key = self.key
        door_name = self.db.door_name

        other_direction = ''

        for direction in direction_dict:
            if direction[0] in door_key:
                other_direction = direction_dict[door_direction][1]
        other_side = self.destination.search(other_direction, typeclass='typeclasses.doors.Door')

        self.db.return_exit = other_side
        other_side.db.return_exit = self

        if named:
            # self.aliases.clear()
            other_side.aliases.clear()

            self.set_door_name(door_name)
            
            self.aliases.add([door_direction, door_name])
            other_side.aliases.add([direction_dict[door_direction][1], door_name])

        if same_desc:
            other_side.db.desc = self.db.desc

    def delete(self):
        """
        Deletes both sides of the door.

        """
        # we have to be careful to avoid a delete-loop.
        if self.db.return_exit:
            super().delete()
        super().delete()
        return True

    def open(self):
        if not self.db.is_open:
            self.db.is_open = True
            self.db.return_exit.db.is_open = True

    def close(self):
        if self.db.is_open:
            self.db.is_open = False
            self.db.return_exit.db.is_open = False            

    def get_display_name(self, looker=None, **kwargs):
        mode = kwargs.get('mode')
        if mode == 'dir':
            display_name = f"({self.name})" if self.db.is_open else f"[{self.name}]"
            return (
                (f"{display_name}" + f"({self.dbref})")
                if looker.locks.check_lockstring(looker, "_dummy:perm(Builder)")
                else f"{display_name}"
            )
        
        display_name = parser.parse(f"$an({self.db.door_name})").title() if self.db.door_name[-1] != 's' else self.db.door_name.title()
        
        # Check for Builder permission. If valid, display dbref (#XYZ)
        if looker:
            if looker.locks.check_lockstring(looker, "_dummy:perm(Builder)"):
                display_name +=  f"({self.dbref})"
        return display_name

    def get_display_desc(self, looker, **kwargs):
        desc = self.db.desc, self.db.desc_state
        return iter_to_multiline(desc)
        