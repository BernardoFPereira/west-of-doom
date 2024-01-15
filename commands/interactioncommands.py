from commands.command import MuxCommand
# import evennia
# from evennia import default_cmds
from evennia import CmdSet

class CmdObjOpen(MuxCommand):
    '''
    Open things!

    Usage:
        open <something>
        open exit <direction>
    '''
    help_category = "Interactions"

    key = 'open'
    aliases = ['op', 'ope']
    rhs_split = " "

    def parse(self):
        super().parse()
        self.exit = False

        if not self.args:
            self.target = ''
        elif self.lhs == 'exit':
            self.target = self.rhs
            self.exit = True
        else:
            self.target = self.args

    def func(self):
        target = self.caller.search(self.target, exact=True, quiet=True)

        if self.exit:
            target = self.caller.search(self.target, typeclass='typeclasses.doors.Door', exact=True, quiet=True, )
        
        if not target:
            return self.msg("Open what?")

        target = target[0]

        if not self.exit:
            # check if args is something like 'w' or 'west', if so, check that 'w' is in target's aliases
            if len(self.args) == 1 or self.args[0] in target.aliases.all():
                return self.msg("Open what?")

        target_name = target.get_display_name() if not target.db.door_name else target.db.door_name

        if target.db.is_open == False:
            open_msg = f"$You() $conj(open) the {target_name}."

            if self.exit:
                target_name = target.db.door_name
                target.destination.msg_contents(f"Someone opened the {target_name} from the other side")

            target.open()
            target.set_state(f"The {target_name} is open." if target_name[-1] != 's' else f"The {target_name} are open.")
            self.caller.location.msg_contents(open_msg, from_obj=self.caller)
            return
        
        self.msg(
            (f"The {target_name} is already open!" if target_name[-1] != 's' else f"The {target_name} are already open!")
            if (target.is_typeclass('typeclasses.containers.Container') or target.is_typeclass('typeclasses.doors.Door'))
            else "You can't open that!"
            )


class CmdObjClose(MuxCommand):
    '''
    Close things!

    Usage:
        close <something>
        close exit <direction>
    '''
    help_category = "Interactions"

    key = 'close'
    aliases = ['cl', 'clo']
    rhs_split = " "

    def parse(self):
        super().parse()
        self.exit = False

        if not self.args:
            self.target = ''
        elif self.lhs == 'exit':
            self.target = self.rhs
            self.exit = True
        else:
            self.target = self.args

    def func(self):
        target = self.caller.search(self.target, exact=True, quiet=True)

        if self.exit:
            target = self.caller.search(self.target, typeclass='typeclasses.doors.Door', exact=True, quiet=True)

        if not target:
            return self.msg("Close what?")
        
        target = target[0]

        if not self.exit:
            if len(self.target) == 1 or self.target[0] in target.aliases.all():
                return self.msg("Close what?")
        
        target_name = target.get_display_name() if not target.db.door_name else target.db.door_name
        
        if target.db.is_open:
            close_msg = f"$You() $conj(close) the {target_name}."

            if self.exit:
                target_name = target.db.door_name
                target.destination.msg_contents(f"Someone closed the {target_name} from the other side")

            target.close()
            target.set_state(f"The {target_name} is closed." if target_name[-1] != 's' else f"The {target_name} are closed.")
            self.caller.location.msg_contents(close_msg, from_obj=self.caller)
            return
        
        self.msg(
            (f"The {target_name} is already closed!" if target_name[-1] != 's' else f"The {target_name} are already closed!")
            if (target.is_typeclass('typeclasses.containers.Container') or target.is_typeclass('typeclasses.doors.Door'))
            else "You can't close that!"
            )


class CmdPut(MuxCommand):
    '''
    Store items in containers.

    Usage:
        put <item> <container>
    '''
    help_category = "Interactions"

    key = 'put'
    aliases = ['p','pu']
    rhs_split = " "

    def func(self):
        caller = self.caller

        item = self.lhs
        container = self.rhs

        if not self.args:
            return caller.msg('Put what? Where?')
        
        targ_item = caller.search(item, candidates=caller.contents, quiet=True)
        
        if not targ_item:
            return caller.msg("You're not carrying any of that!")

        if not container:
            return caller.msg('Where?')
        
        targ_container = caller.search(container)

        if not targ_container:
            return caller.msg(f"There's no '{container}' around.")
        
        if not targ_container.is_typeclass('typeclasses.containers.Container'):
            return caller.msg("You can't do that!")
        
        if not targ_container.db.is_open:
            return caller.msg(f"The {targ_container.name} is closed!")

        targ_item[0].location = targ_container

        caller.location.msg_contents(f"$You() $conj(put) $obj(target) in the $obj(container).",
                                     from_obj=caller,
                                     mapping={'target':targ_item[0].get_numbered_name(1,caller)[0],'container':targ_container.get_display_name()}
                                    )


class CustomCmdGet(MuxCommand):
    """
    Pick up something from the ground or
    from containers and put it in your inventory.

    Usage:
      get <item>
      get <item> <container>
    """
    help_category = "Interactions"
    
    key = "get"
    aliases = ["grab", 'g']
    rhs_split = (" ", " from ")
    locks = "cmd:all();view:perm(Developer);read:perm(Developer)"
    arg_regex = r"\s|$"

    def func(self):
        """implements the command."""

        caller = self.caller

        item = self.lhs
        container = self.rhs

        if not self.args:
            caller.msg("Get what?")
            return
        
        targ_item = caller.search(item, location=caller.location, quiet=True)

        if container:
            targ_container = caller.search(container, quiet=True)

            if not targ_container:
                return caller.msg(f"There's no '{container}' around.")

            if not targ_container[0].is_typeclass('typeclasses.containers.Container'):
                return caller.msg(f"You can't do that!")
            
            if not targ_container[0].db.is_open:
                return caller.msg(f"The {targ_container[0].name} is closed!")
            
            targ_item = caller.search(item, location=targ_container[0], quiet=True) 

            if not targ_item:
                return caller.msg(f"Could not find any '{item}' inside the {targ_container[0].name}!")
                        
        if not targ_item:
            return caller.msg(f"Could not find any '{item}'.")
                
        if caller == targ_item[0]:
            caller.msg("You can't get yourself.")
            return
        
        if not targ_item[0].access(caller, "get"):
            if targ_item[0].db.get_err_msg:
                caller.msg(targ_item[0].db.get_err_msg)
            else:
                caller.msg("You can't get that.")
            return

        # calling at_pre_get hook method
        if not targ_item[0].at_pre_get(caller):
            return
        
        success = targ_item[0].move_to(caller, quiet=True, move_type="get")

        if not success:
            caller.msg("You can't get it.")
        else:
            singular, _ = targ_item[0].get_numbered_name(1, caller)
            caller.location.msg_contents(
                (f"$You() $conj(pick) up {singular}."
                if not container else
                f"$You() $conj(pick) up {singular} from the {targ_container[0].name}."),
                from_obj = caller,
            )
            # calling at_get hook method
            targ_item[0].at_get(caller)


class InteractionsCmdSet(CmdSet):

    key = 'ObjectInteraction'

    def at_cmdset_creation(self):
        self.add(CmdObjOpen)
        self.add(CmdObjClose)
        self.add(CmdPut)
        self.add(CustomCmdGet)
