from evennia import CmdSet, default_cmds#, syscmdkeys
from commands.command import MuxCommand
from utils.utils import make_iter, iter_to_multiline
from enums import WieldLocations, WearLocations
import random

class CmdEcho(MuxCommand):
    '''
    A simple echo command

    Usage:
        echo <something>
    '''
    key = 'echo'

    def func(self):
        self.caller.msg(f"Echo: {self.args.strip()}")
        
class CmdExamine(MuxCommand):
    '''
    Carefully |yexamine|n an object or creature.
    
    Usage:
        examine <target>
    '''

    key = 'examine'
    help_category = 'Exploring'
    aliases = ['exam', 'exa']
    locks = "cmd:all()"

    def parse(self):
        args = self.args.strip()
        if not args:
            self.target = ""
        else:
            self.target = args
        # target = self.args.split(" ", 1)
        # self.target = target[0].strip()
    
    def func(self):
        caller = self.caller

        if not self.target:
            self.msg("Examine what?")
            return
        
        # self.msg(f"Examining {self.target}")
        target = caller.search(self.target)

        if not target:
            return
        
        if target.is_typeclass('typeclasses.containers.Container'):
            if target.db.is_open == False:
                _, state = target.get_display_desc(looker=caller).split("\n")
                # self.msg(f"|b{target.get_display_name(looker=caller).capitalize()}|n")
                self.msg(state)
            else:
                # self.msg(f"|b{target.get_display_name(looker=caller).capitalize()}|n")
                # self.msg(target.return_appearance(looker=caller))
                # self.msg(target.get_display_desc(looker=caller))
                self.msg(target.get_display_things(looker=caller, examination=True))
            return

        if target.is_typeclass('typeclasses.weapons.Weapon'):
            self.msg(f"|b{target.get_display_name(looker=caller)}|n")
            # self.msg(target.return_appearance(looker=caller))
            self.msg(target.get_display_things(looker=caller, examination=True))
            return

        self.msg(target.return_appearance(looker=caller))
        # self.msg(target.get_display_name(looker=caller))
        # self.msg(target.get_display_desc(looker=caller))
        self.msg(target.get_display_things(looker=caller, examination=True))
        
        if target.is_typeclass('typeclasses.characters.Character'):
            self.msg(target.return_condition_string())
            return

class CmdFollow(MuxCommand):
    '''
    Follow someone. Every time your 'follow target' moves
    to a different room you will move right after.

    Usage:
        follow <target>
        unfollow
    '''
    help_category = "General"
    key = 'follow'

    def parse(self):
        args = self.args.strip()
        if not args:
            self.target = ""
        else:
            self.target = args
    
    def func(self):
        caller = self.caller
        
        if not self.target:
            self.caller.msg("Follow who?")
            return
        
        target = self.caller.search(self.target)
        if target:
            caller.ndb.follow_target = target
            
        caller.msg(f"Following {target.get_display_name()}.")

class CmdInfo(MuxCommand):
    pass

class CmdHit(MuxCommand):
    '''
    Hit someone or something.

    Usage:
        hit <target>
    '''
    help_category = "Combat"
    key = 'hit'
    aliases = ['h', 'kill', 'kil', 'k']

    # def parse(self):
    #     self.args = self.args.strip()
    #     target, *weapon = self.args.split(" with ", 1)
    #     if not weapon:
    #         target, *weapon = target.split(" ", 1)
    #     self.target = target.strip()
    #     if weapon:
    #         self.weapon = weapon[0].strip()
    #     else:
    #         self.weapon = ""
    def parse(self):
        self.args = self.args.strip()
        target = self.args
        self.target = target.strip()

    def func(self):
        caller = self.caller
        weapon = None
        
        if not self.args:
            self.caller.msg('Hit who?')
            return
        
        target = self.caller.search(self.target)
        if not target:
            return

        caller_weapon = [
            eq for eq in caller.equipment.all()
            if eq[0] is not None and (eq[1] == WieldLocations.MAIN_HAND or eq[1] == WieldLocations.TWO_HANDS)
        ]
        
        # weapon = caller.search(self.weapon, typeclass='typeclasses.weapons.Weapon',quiet=True)
        damage = caller.body * 0.4
        weaponstr = 'bare fists'
            
        if caller_weapon:
            weapon = caller_weapon[0][0]
            weaponlst = make_iter(weapon.aliases)
            weaponstr = str(weaponlst[0]).split(",",1)
            weaponstr = weaponstr[0]
            damage = int((weapon.weight * caller.body * 0.4) * (random.uniform(0.9, 1.1)))

        # Self msg
        caller.location.msg_contents(
            f"|BYou hit $you(target) with $obj(weapon)!\n|RDamage: {damage}",
            exclude=[obj for obj in caller.location.contents if obj.key != caller.key],
            mapping = {
                'target':target.get_display_name(looker=caller),
                'weapon':weaponstr}
            )
        # Onlookers msg
        caller.location.msg_contents(
            "$You(caller) $conj(hit) $you(target) with $obj(weapon)!",
            exclude=[caller, target],
            mapping={
                'caller':caller.get_display_name(),
                'target':target.get_display_name(),
                'weapon':weaponstr}
            )
        # Target msg
        target.location.msg_contents(
            f"|R$You(caller) hits you with $obj(weapon)!|n\n|RDamage: {damage}",
            exclude = [obj for obj in caller.location.contents if obj.key != target.key],
            mapping={
                'caller':caller.get_display_name(),
                'weapon':weaponstr}
            )

class CmdSwim(MuxCommand):
    '''
    Turns |hswimming|n on and off.
    When |hswim|n is active, you'll not be warned when getting
    into |B~water~|n.
    Using |Yswim always|n will ignore the strength of the water
    current if there is any.
    [NOT IMPLEMENTED YET]
    Usage:
        swim
        *from here on is not implemented yet
        swim safe
        swim always
    '''
    help_category = "Exploring"
    key = 'swim'

    def func(self):
        caller = self.caller
        # args = self.args <- useful later? maybe implement 'swim safe' when river flow is implemented

        if not caller.db.will_swim:
            caller.db.will_swim = True
            return self.msg("You'll enter water automatically from now on...")
            
        caller.db.will_swim = False
        return self.msg("You'll no longer enter water automatically.")

class CmdSneak(MuxCommand):
    '''
    When |hsneak|n is active, you'll try to move silently.
    This makes you move slower(spends more |Gmove points|n),
    but harder to spot.
    [NOT IMPLEMENTED YET]
    Usage:
        sneak
    '''
    help_category = "Exploring"
    key = 'sneak'

    def func(self):
        caller = self.caller
        sneaking = caller.ndb.sneaking

        if not sneaking:
            caller.ndb.sneaking = True
            return self.msg("You will try to move silently from now on...")
        
        del caller.ndb.sneaking
        return self.msg("You will no longer try to move silently.")
    

class CmdApproach(MuxCommand):
    help_category = "Combat"
    key = 'approach'

    def func(self):
        caller = self.caller
        args = self.args.strip()
        
        if not args:
            return self.msg("Approach what?")
        
        target = caller.search(args)
        
        if target:
            caller.ndb.near = []
            

            if not target.ndb.near_you:
                target.ndb.near_you = []
            else:
                target.ndb.near_you.remove(caller)
                
            caller.ndb.near.append(target)
            target.ndb.near_you.append(caller)
            
            return self.msg(f"You approach {target.get_display_name()}.")
        

class CmdAvoid(MuxCommand):
    help_category = "Combat"
    key = 'avoid'

    def func(self):
        caller = self.caller
        args = self.args.strip()
        
        if not args:
            return self.msg("Avoid what?")
            
        target = caller.search(args)

        if target:
            if caller.ndb.near:
                del caller.ndb.near
                return self.msg(f"You distance yourself from {target.get_display_name()}.")

class CmdNear(MuxCommand):
    help_category = "Combat"
    key = 'near'

    def func(self):
        caller = self.caller
        near_objects = []
        
        if caller.ndb.near:
            near_objects += [obj.get_display_name() for obj in caller.ndb.near]

        if caller.ndb.near_you:
            near_objects += [obj.get_display_name() for obj in caller.ndb.near_you]
            
        self.msg(f"|wNear you:|n\n {iter_to_multiline(near_objects, "\n ")}")
        
        if not caller.ndb.near and not caller.ndb.near_you:
            return self.msg("There is nobody near you.")

class StandardCmdSet(CmdSet):
    key = "Standard cmd_set"
    def at_cmdset_creation(self):
        self.add([
                 CmdExamine,
                 CmdEcho,
                 CmdHit,
                 CmdSwim,
                 CmdSneak,
                 CmdFollow,
                 CmdApproach,
                 CmdAvoid,
                 CmdNear,
             ])
