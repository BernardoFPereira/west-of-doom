# !!!UNUSED!!!

from commands.command import Command
from evennia import CmdSet

class CmdDoorOpen(Command):
    '''
    Open things!

    Usage:
        open <something>
    '''
    key = 'open'
    aliases = ['op']

    def parse(self):
        self.args = self.args.strip()
        if not self.args:
            self.exit = ''
        else:
            self.exit = self.args

    def func(self):
        target = self.caller.search(self.exit, quiet=True)
        if not target:
            self.msg("Open what?")
            return
        
        if target[0].is_typeclass('typeclasses.doors.Door'):
            open_type = 'door'
            target = target[0]
            door_name = target.db.door_name

        if not target.db.is_open:
            self.caller.location.msg_contents(
                f"$You() $conj(open) the {target.get_display_name() if open_type != 'door' else door_name}.",
                from_obj=self.caller
                )
            target.open_door()
            if open_type == 'door':
                target.destination.msg_contents(f"Someone opened the {door_name} from the other side")
            target.set_state(f"The {door_name} is open." if door_name[-1] != 's' else f"The {door_name} are open.")
            return
        self.msg(f"The {door_name} is already open!" if door_name[-1] != 's' else f"The {door_name} are already open!")
        
class CmdDoorClose(Command):
    '''
    Close things!

    Usage:
        close <something>
    '''
    key = 'close'
    aliases = ['cl']

    def parse(self):
        self.args = self.args.strip()
        if not self.args:
            self.target = ''
        else:
            self.target = self.args

    def func(self):
        target = self.caller.search(self.target, quiet=True)
        if not target:
            self.msg("Close what?")
            return
        if target[0].is_typeclass('typeclasses.doors.Door'):
            door = target[0]
            door_name = door.db.door_name

        if door.db.is_open:
            self.caller.location.msg_contents(
                f"$You() $conj(close) the {door_name}.",
                exclude=self.caller,
                from_obj=self.caller.get_display_name()
                )
            door.close_door()
            self.msg(f"You close the {door_name}.")
            door.destination.msg_contents(f"Someone closed the {door_name} from the other side")
            door.set_state(f"The {door_name} is closed." if door_name[-1] != 's' else f"The {door_name} are closed.")
            return
        self.msg(f"The {door_name} is already closed!" if door_name[-1] != 's' else f"The {door_name} are already closed!")

class DoorCmdSet(CmdSet):

    key = 'DoorInteraction'

    def at_cmdset_creation(self):
        self.add(CmdDoorOpen)
        self.add(CmdDoorClose)
