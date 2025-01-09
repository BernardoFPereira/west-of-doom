from evennia import Command
from commands.command import MuxCommand
from evennia import CmdSet, default_cmds, syscmdkeys

from evennia.utils.utils import crop
from utils.utils import make_iter
from random import randint

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
        
        if target and target.is_typeclass('typeclasses.containers.Container'):
            if target.db.is_open == False:
                _, state = target.get_display_desc(looker=caller).split("\n")
                self.msg(state)
            else:
                self.msg(f"|b{target.get_display_name(looker=caller).capitalize()}|n")
                self.msg(target.return_appearance(looker=caller))
                # self.msg(target.get_display_desc(looker=caller))
                self.msg(target.get_display_things(looker=caller, examination=True))
            return

        self.msg(target.return_appearance(looker=caller))
        # self.msg(target.get_display_name(looker=caller))
        # self.msg(target.get_display_desc(looker=caller))
        self.msg(target.get_display_things(looker=caller, examination=True))

class CmdHit(MuxCommand):
    '''
    Hit someone or something.

    Usage:
        hit <target>
    '''
    help_category = "Combat"
    key = 'hit'
    aliases = ['h', 'kill', 'kil', 'k']

    def parse(self):
        self.args = self.args.strip()
        target, *weapon = self.args.split(" with ", 1)
        if not weapon:
            target, *weapon = target.split(" ", 1)
        self.target = target.strip()
        if weapon:
            self.weapon = weapon[0].strip()
        else:
            self.weapon = ""

    def func(self):
        if not self.args:
            self.caller.msg('Hit who?')
            return
        target = self.caller.search(self.target)
        if not target:
            return
            
        weapon = None

        if self.weapon:
            weapon = self.caller.search(self.weapon, typeclass='typeclasses.weapons.Weapon',quiet=True)
        if weapon:
            weaponlst = make_iter(weapon[0].aliases)
            weaponstr = str(weaponlst[0]).split(",",1)
            weaponstr = weaponstr[0]

        else:
            weaponstr = 'bare fists'

        # Self msg
        self.caller.location.msg_contents(
            "|BYou hit $you(target) with $obj(weapon)!",
            exclude=[obj for obj in self.caller.location.contents if obj.key != self.caller.key],
            mapping = {
                'target':target.get_display_name(looker=self.caller),
                'weapon':weaponstr}
            )
        # Onlookers msg
        self.caller.location.msg_contents(
            "$You(caller) $conj(hit) $you(target) with $obj(weapon)!",
            exclude=[self.caller, target],
            mapping={
                'caller':self.caller.get_display_name(),
                'target':target.get_display_name(),
                'weapon':weaponstr}
            )
        # Target msg
        target.location.msg_contents(
            "|R$You(caller) hits you with $obj(weapon)!|n",
            exclude = [obj for obj in self.caller.location.contents if obj.key != target.key],
            mapping={
                'caller':self.caller.get_display_name(),
                'weapon':weaponstr}
            )

class CmdSwim(MuxCommand):
    '''
    Turns |hswimming|n on and off.
    When |hswim|n is active, you'll not be warned when getting
    into |~Bwater~|n.
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

class CmdEquipment(MuxCommand):
    """
    view equipped items

    Usage:
      equipment
      equip
      eq

    Shows your inventory(for now).
    """
    
    key = "equipment"
    aliases = ["equip", "eq"]
    locks = "cmd:all()"
    arg_regex = r"$"

    def func(self):
        """check equipment, for now it's inventory"""
        items = self.caller.contents
        if not items:
            string = "You are not wearing anything."
        else:
            # from evennia.utils.ansi import raw as raw_ansi

            table = self.styled_table(border="header")
            for item in items:
                singular, _ = item.get_numbered_name(1, self.caller)
                table.add_row(
                    f"|C{singular}|n",
                    # "{}|n".format(crop(raw_ansi(item.db.desc or ""), width=50) or ""),
                )
            string = f"|wYour gear:\n{table}"
        self.caller.msg(text=(string, {"type": "equipment"}))

    # def handle_attack(self, target, weaponstr, hit, damage):
    #     if damage == 0:
    #         damage = 'no'
    #     if hit:
    #         # Self msg
    #         self.caller.location.msg_contents(
    #             f"|BYou hit $you(target) with $obj(weapon) for {damage} damage!",
    #             exclude=[obj for obj in self.caller.location.contents if obj.key != self.caller.key],
    #             mapping = {
    #                 'target':target.get_display_name(mode='emote'),
    #                 'weapon':weaponstr}
    #             )
    #         # Onlookers msg
    #         self.caller.location.msg_contents(
    #             f"$You(caller) $conj(hit) $you(target) with $obj(weapon) for {damage} damage!",
    #             exclude=[self.caller, target],
    #             mapping={
    #                 'caller':self.caller.get_display_name(mode='emote'),
    #                 'target':target.get_display_name(mode='emote'),
    #                 'weapon':weaponstr}
    #             )
    #         # Target msg
    #         target.location.msg_contents(
    #             f"|R$you(caller) hits you with $obj(weapon) for {damage} damage!|n",
    #             exclude = [obj for obj in self.caller.location.contents if obj.key != target.key],
    #             mapping={
    #                 'caller':self.caller.get_display_name(mode='emote'),
    #                 'weapon':weaponstr}
    #             )
    #     if not hit:
    #         # Self msg
    #         self.caller.location.msg_contents(
    #             f"|BYou try to hit $you(target) with $obj(weapon) but miss!",
    #             exclude=[obj for obj in self.caller.location.contents if obj.key != self.caller.key],
    #             mapping = {
    #                 'target':target.get_display_name(mode='emote'),
    #                 'weapon':weaponstr}
    #             )
    #         # Onlookers msg
    #         self.caller.location.msg_contents(
    #             f"$You(caller) $conj(try) $conj(hit) $you(target) with $obj(weapon) but misses!",
    #             exclude=[self.caller, target],
    #             mapping={
    #                 'caller':self.caller.get_display_name(mode='emote'),
    #                 'target':target.get_display_name(mode='emote'),
    #                 'weapon':weaponstr}
    #             )
    #         # Target msg
    #         target.location.msg_contents(
    #             f"|R$you(caller) tries to hit you with $obj(weapon) but misses!|n",
    #             exclude = [obj for obj in self.caller.location.contents if obj.key != target.key],
    #             mapping={
    #                 'caller':self.caller.get_display_name(mode='emote'),
    #                 'weapon':weaponstr}
    #             )

class MyNoInputCommand(Command):
    "Usage: Just press return, I dare you"
    key = syscmdkeys.CMD_NOINPUT
    def func(self):
        caller = self.caller
        return self.msg(prompt=caller.prompt)

class MyCmdSet(CmdSet):
    key = "Main test cmd_set"
    def at_cmdset_creation(self):
        self.add(CmdExamine)
        self.add(CmdEcho)
        self.add(CmdHit)
        self.add(CmdSwim)
        self.add(CmdSneak)
        self.add(CmdEquipment)
        self.add(MyNoInputCommand)
