from evennia import CmdSet
from commands.command import MuxCommand
from utils.utils import is_sitting_msg

class ExitErrorCmd(MuxCommand):
    '''
    Parent class for all exit errors.
    '''
    auto_help = False
    def func(self):
        caller = self.caller
        if caller.db.stance == 'sitting':
            return is_sitting_msg(caller)

        caller.msg(f"Shucks! No way {self.key}, it seems.")
    
class ErrorNorthCmd(ExitErrorCmd):
    key = 'north'
    aliases = ['n']

class ErrorSouthCmd(ExitErrorCmd):
    key = 'south'
    aliases = ['s']

class ErrorEastCmd(ExitErrorCmd):
    key = 'east'
    aliases = ['e']

class ErrorWestCmd(ExitErrorCmd):
    key = 'west'
    aliases = ['w']

class ErrorUpCmd(ExitErrorCmd):
    key = 'up'
    aliases = ['u']

class ErrorDownCmd(ExitErrorCmd):
    key = 'down'
    aliases = ['d']

class MovementFailCmdSet(CmdSet):
    key = "MovementFail"
    def at_cmdset_creation(self):
        self.add(ErrorNorthCmd)
        self.add(ErrorSouthCmd)
        self.add(ErrorEastCmd)
        self.add(ErrorWestCmd)
        self.add(ErrorUpCmd)
        self.add(ErrorDownCmd)