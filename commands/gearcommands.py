from commands.command import MuxCommand
from evennia import CmdSet

class CmdWear(MuxCommand):
    """
    Wear equippable items

    Usage:
        wear <item>
        wear <item> <slot> !! Not implemented !!
        
    """
    key = 'wear'
    category = 'Equipment'

    # Search item in self.location(inventory) or room
    # Mark item as equipped so it won't show when print inventory
    
    pass

class CmdRemove(MuxCommand):
    """
    Remove equipped items

    Usage:
        remove <item>
        remove <slot> !! Not implemented !!
        
    """
    key = 'remove'
    aliases = ['rem']
    category = 'Equipment'

    # Search equipped item in self.location
    # Unmark item as equipped so it show when print inventory
    
    pass

class GearCmdSet(CmdSet):
    key = "Main test cmd_set"
    def at_cmdset_creation(self):
        self.add([
                 CmdWear,
                 CmdRemove
             ])
