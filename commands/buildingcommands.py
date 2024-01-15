from unicodedata import category
from evennia import default_cmds, CmdSet
from evennia.utils import inherits_from, create
from typeclasses.doors import Door
from django.conf import settings
# from evennia.commands.default.muxcommand import MuxCommand as DefaultMuxCommand

class BuildingCmdOpen(default_cmds.CmdOpen):
    __doc__ = default_cmds.CmdOpen.__doc__
    # overloading parts of the default CmdOpen command to support doors.

    def create_exit(self, exit_name, location, destination, exit_aliases=None, typeclass=None):
        """
        Simple wrapper for the default CmdOpen.create_exit
        """
        # create a new exit as normal
        new_exit = super().create_exit(
            exit_name, location, destination, exit_aliases=exit_aliases, typeclass=typeclass
        )
        if hasattr(self, "return_exit_already_created"):
            # we don't create a return exit if it was already created (because
            # we created a door)
            del self.return_exit_already_created
            return new_exit
        if inherits_from(new_exit, Door):
            # a door - create its counterpart and make sure to turn off the default
            # return-exit creation of CmdOpen
            self.caller.msg(
                "Note: A door-type exit was created - ignored eventual custom return-exit type."
            )
            self.return_exit_already_created = True
            back_exit = self.create_exit(
                exit_name, destination, location, exit_aliases=exit_aliases, typeclass=typeclass
            )
            new_exit.db.return_exit = back_exit
            back_exit.db.return_exit = new_exit
        return new_exit


class BuildingCmdDig(default_cmds.CmdDig):
    __doc__ = default_cmds.CmdDig.__doc__

    key = "@dig"
    switch_options = ("teleport",)

    def func(self):
        """Do the digging. Inherits variables from ObjManipCommand.parse()"""

        caller = self.caller
        location = self.caller.location
        
        location_coordx = int(location.tags.get(category="coordx"))
        location_coordy = int(location.tags.get(category="coordy"))
        location_coordz = int(location.tags.get(category="coordz"))

        if not self.lhs:
            string = "Usage: dig[/teleport] <roomname>[;alias;alias...][:parent] [= <exit_there>"
            string += "[;alias;alias..][:parent]] "
            string += "[, <exit_back_here>[;alias;alias..][:parent]]"
            caller.msg(string)
            return

        room = self.lhs_objs[0]

        if not room["name"]:
            caller.msg("You must supply a new room name.")
            return
        location = caller.location

        # Create the new room
        typeclass = room["option"]
        if not typeclass:
            typeclass = settings.BASE_ROOM_TYPECLASS

        # create room
        new_room = create.create_object(
            typeclass, room["name"], aliases=room["aliases"], report_to=caller
        )
        lockstring = self.new_room_lockstring.format(id=caller.id)
        new_room.locks.add(lockstring)
        alias_string = ""
        if new_room.aliases.all():
            alias_string = " (%s)" % ", ".join(new_room.aliases.all())
        room_string = (
            f"Created room {new_room}({new_room.dbref}){alias_string} of type {typeclass}."
        )

        # create exit to room

        exit_to_string = ""
        exit_back_string = ""

        if self.rhs_objs:
            to_exit = self.rhs_objs[0]
            if not to_exit["name"]:
                exit_to_string = "\nNo exit created to new room."
            elif not location:
                exit_to_string = "\nYou cannot create an exit from a None-location."
            else:
                # Build the exit to the new room from the current one
                typeclass = to_exit["option"]
                if not typeclass:
                    typeclass = settings.BASE_EXIT_TYPECLASS

                new_to_exit = create.create_object(
                    typeclass,
                    to_exit["name"],
                    location,
                    aliases=to_exit["aliases"],
                    locks=lockstring,
                    destination=new_room,
                    report_to=caller,
                )
                alias_string = ""
                if new_to_exit.aliases.all():
                    alias_string = " (%s)" % ", ".join(new_to_exit.aliases.all())
                exit_to_string = (
                    f"\nCreated Exit from {location.name} to {new_room.name}:"
                    f" {new_to_exit}({new_to_exit.dbref}){alias_string}."
                )

        # Create exit back from new room

        if len(self.rhs_objs) > 1:
            # Building the exit back to the current room
            back_exit = self.rhs_objs[1]
            if not back_exit["name"]:
                exit_back_string = "\nNo back exit created."
            elif not location:
                exit_back_string = "\nYou cannot create an exit back to a None-location."
            else:
                typeclass = back_exit["option"]
                if not typeclass:
                    typeclass = settings.BASE_EXIT_TYPECLASS
                new_back_exit = create.create_object(
                    typeclass,
                    back_exit["name"],
                    new_room,
                    aliases=back_exit["aliases"],
                    locks=lockstring,
                    destination=location,
                    report_to=caller,
                )
                alias_string = ""
                if new_back_exit.aliases.all():
                    alias_string = " (%s)" % ", ".join(new_back_exit.aliases.all())
                exit_back_string = (
                    f"\nCreated Exit back from {new_room.name} to {location.name}:"
                    f" {new_back_exit}({new_back_exit.dbref}){alias_string}."
                )
                # MY TEST ADD-ON
                if inherits_from(new_back_exit, Door):
                    new_back_exit.connect_other_side()

        caller.msg(f"{room_string}{exit_to_string}{exit_back_string}")

        if new_room and "teleport" in self.switches:
            caller.move_to(new_room, move_type="teleport")

        new_room.x = (location_coordx + 1 if new_to_exit.name == 'east'
                      else location_coordx - 1 if new_to_exit.name == 'west'
                      else location_coordx)
        new_room.y = (location_coordy + 1 if new_to_exit.name == 'north'
                      else location_coordy - 1 if new_to_exit.name == 'south'
                      else location_coordy)
        new_room.z = (location_coordz + 1 if new_to_exit.name == 'up'
                      else location_coordz - 1 if new_to_exit.name == 'down'
                      else location_coordz)


class MyBuildingCmdSet(CmdSet):
    def at_cmdset_creation(self):
        self.add(BuildingCmdOpen)
        self.add(BuildingCmdDig)
