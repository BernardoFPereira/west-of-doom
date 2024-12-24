"""
Exits

Exits are connectors between Rooms. An exit always has a destination property
set and has a single command defined on itself with the same name as its key,
for allowing Characters to traverse the exit to its destination.

"""
from evennia.objects.objects import DefaultExit
from utils.utils import is_sitting_msg
from .objects import ObjectParent


class Exit(ObjectParent, DefaultExit):
    """
    Exits are connectors between rooms. Exits are normal Objects except
    they defines the `destination` property. It also does work in the
    following methods:

     basetype_setup() - sets default exit locks (to change, use `at_object_creation` instead).
     at_cmdset_get(**kwargs) - this is called when the cmdset is accessed and should
                              rebuild the Exit cmdset along with a command matching the name
                              of the Exit object. Conventionally, a kwarg `force_init`
                              should force a rebuild of the cmdset, this is triggered
                              by the `@alias` command when aliases are changed.
     at_failed_traverse() - gives a default error message ("You cannot
                            go there") if exit traversal fails and an
                            attribute `err_traverse` is not defined.

    Relevant hooks to overload (compared to other types of Objects):
        at_traverse(traveller, target_loc) - called to do the actual traversal and calling of the other hooks.
                                            If overloading this, consider using super() to use the default
                                            movement implementation (and hook-calling).
        at_post_traverse(traveller, source_loc) - called by at_traverse just after traversing.
        at_failed_traverse(traveller) - called by at_traverse if traversal failed for some reason. Will
                                        not be called if the attribute `err_traverse` is
                                        defined, in which case that will simply be echoed.
    """
    def at_failed_traverse(self, traversing_object, **kwargs):

        if kwargs.get('not_standing'):
            return is_sitting_msg(traversing_object)
        
        if kwargs.get('door_closed'):
            return traversing_object.msg(
                f"The {self.db.door_name} is closed!" if self.db.door_name[-1] != 's'
                else f"The {self.db.door_name} are closed."
                )
        
        return super().at_failed_traverse(traversing_object, **kwargs)

    def at_traverse(self, traversing_object, target_location):

        if traversing_object.db.stance == 'sitting':
            self.at_failed_traverse(traversing_object,not_standing=True)
            return
        
        if self.db.is_open == False:
            self.at_failed_traverse(traversing_object,door_closed=True)
            return
        
        return super().at_traverse(traversing_object, target_location)
    
    def get_display_name(self, looker=None, **kwargs):
        mode = kwargs.get('mode')
        display_name = self.name

        if mode == 'dir':
            return (
                display_name + f"({self.dbref})"
                if looker.locks.check_lockstring(looker, "_dummy:perm(Builder)")
                else display_name)
        return (
            (f"{self.key}" + f"({self.dbref})")
            if looker.locks.check_lockstring(looker, "_dummy:perm(Builder)")
            else f"{self.key}")
    

class Road(Exit):
    def at_object_creation(self):        
        self.db.desc = "This is a Road Exit."
        self.db.road_name = 'road'

    def get_display_name(self, looker=None, **kwargs):
        mode = kwargs.get('mode')
        display_name = f"={self.name}="

        if mode == 'dir':
            return (
                display_name + f"({self.dbref})"
                if looker.locks.check_lockstring(looker, "_dummy:perm(Builder)")
                else display_name)
        return (
            (f"{self.key}" + f"({self.dbref})")
            if looker.locks.check_lockstring(looker, "_dummy:perm(Builder)")
            else f"{self.key}")


class Trail(Exit):
    def at_object_creation(self):
        self.db.desc = "This is a Trail Exit."
        self.db.road_name = 'trail'

    def get_display_name(self, looker=None, **kwargs):
        mode = kwargs.get('mode')
        display_name = f"-{self.name}-"

        if mode == 'dir':
            return (
                display_name + f"({self.dbref})"
                if looker.locks.check_lockstring(looker, "_dummy:perm(Builder)")
                else display_name)
        return (
            (f"{self.key}" + f"({self.dbref})")
            if looker.locks.check_lockstring(looker, "_dummy:perm(Builder)")
            else f"{self.key}")
