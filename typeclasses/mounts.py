from typeclasses.characters import Character

from evennia.utils.funcparser import FuncParser
from evennia.utils.funcparser import funcparser_callable_an
# from utils.utils import capitalize_name
from django.utils.translation import gettext as _

parser = FuncParser({"an": funcparser_callable_an})

class Mount(Character):
    '''
    This is a base class for Mounts.
    '''
    _content_types = ("mount", )

    is_pc = False

    def at_object_creation(self):
        self.tags.add('rideable')
        # self.db.stance = 'standing'

    def announce_move_from(self, destination, msg=None, mapping=None, move_type="move",**kwargs):
        if self.ndb.is_ridden:
            return
        return super().announce_move_from(destination, msg, mapping, move_type,**kwargs)

    def announce_move_to(self, source_location, msg=None, mapping=None, move_type="move", **kwargs):
        if not source_location and self.location.has_account:
            # This was created from nowhere and added to an account's
            # inventory; it's probably the result of a create command.
            string = _("You now have {name} in your possession.").format(
                name=self.get_display_name(self.location)
            )
            self.location.msg(string)
            return

        if source_location:
            if msg:
                string = msg
            else:
                string = _("|233{object} has arrived from the {exit}.|n")
        else:
            string = _("|233{object} has suddenly arrived.|n")

        rider = self.ndb.rider
        origin = source_location
        destination = self.location
        exits = []

        if origin:
            exits = [
                o for o in destination.contents
                if o.location is destination and o.destination is origin
            ]

        if not mapping:
            mapping = {}

        mapping.update(
            {
                "object": self.get_display_name() if self.is_typeclass(Character,exact=True) else (self.get_display_name()[0].upper() + self.get_display_name()[1:]),
                "exit": ('below' if exits[0].name == 'down' else 'above' if exits[0].name == 'up' else f"the {exits[0].name}") if exits else "somewhere",
                "origin": origin or "nowhere",
                "destination": destination or "somewhere",
            }
        )

        if rider:
            if self.ndb.is_ridden:
                return
            string = _("|233{object} has arrived from the {exit}.|n")
            destination.msg_contents(
                (string, {"type": move_type}),
                exclude=(self,rider,),
                from_obj=self,
                mapping=mapping
            )
            destination.msg_contents(
                ("|233{object} followed you.|n", {"type": move_type}),
                exclude=[obj for obj in destination.contents if obj.key != rider.key],
                from_obj=self,
                mapping=mapping
            )
            return

        destination.msg_contents(
            (string, {"type": move_type}), exclude=(self, rider,), from_obj=self, mapping=mapping
        )
