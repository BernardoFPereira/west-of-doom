from commands.command import MuxCommand
from evennia import CmdSet
from evennia.utils import crop, group_objects_by_key_and_desc
from enums import WearLocations, WieldLocations
from typeclasses.weapons import Weapon, Ranged

class CmdWear(MuxCommand):
    """
    Wear equippable items

    Usage:
        wear <item>
        wear <item> <slot> !! Not implemented !!
        
    """
    key = 'wear'
    help_category = 'Equipment'

    def parse(self):
        args = self.args.strip()
        if not args:
            self.target = ""
        else:
            self.target = args

    def func(self):
        caller = self.caller

        if not self.target:
            caller.msg("Wear what?")
            return

        target = caller.search(self.target, candidates=caller.contents)
        
        if target and type(target.equipment_use_slot) == WearLocations:
            caller.equipment.add(target)
            caller.equipment.move(target)
            caller.msg(f"You put on {target.get_numbered_name(1, caller)[0]}.")
        else:
            caller.msg("You can't wear that.")

class CmdWield(MuxCommand):
    """
    Wield an object as a weapon

    Usage:
        wield <item>
    
    """
    key = 'wield'
    help_category = 'Equipment'

    def parse(self):
        args = self.args.strip()
        if not args:
            self.target = ""
        else:
            self.target = args

    def func(self):
        caller = self.caller

        if not self.target:
            caller.msg("Wield what?")
            return
        
        possible_targets = caller.search(self.target, candidates=caller.contents, quiet=True)
        target = None

        for possible_target in possible_targets:
            if type(possible_target) == Weapon or type(possible_target) == Ranged:
                target = possible_target
            else:
                continue
        
        if target and type(target.equipment_use_slot) == WieldLocations:
            caller.equipment.add(target)
            caller.equipment.move(target)
            caller.msg(f"You start wielding {target.get_numbered_name(1, caller)[0]}.")
        else:
            caller.msg("You can't wield that.")


class CmdRemove(MuxCommand):
    """
    Remove equipped items

    Usage:
        remove <item>
        remove <slot> !! Not implemented !!
        
    """
    key = 'remove'
    aliases = ['rem']
    help_category = 'Equipment'

    def parse(self):
        args = self.args.strip()
        if not args:
            self.target = ""
        else:
            self.target = args

    def func(self):
        caller = self.caller

        if not self.target:
            caller.msg("Wear what?")
            return

        target = caller.search(self.target, candidates=caller.contents)
        if target:
            caller.equipment.remove(target)
            
            if type(target.equipment_use_slot) == WieldLocations:
                caller.msg(f"You stop wielding {target.get_numbered_name(1, caller)[0]}.")
            else:
                caller.msg(f"You take off {target.get_numbered_name(1, caller)[0]}.")
                

class CmdInventory(MuxCommand):
    """
    view inventory

    Usage:
      inventory
      inv

    Shows your inventory.
    """

    key = "inventory"
    aliases = ["inv", "i"]
    locks = "cmd:all()"
    arg_regex = r"$"

    def func(self):
        """check inventory"""
        items = [i for i in self.caller.contents if i not in self.caller.equipment.slots.values()]
        
        if not items:
            string = "You are not carrying anything."
        else:
            from evennia.utils.ansi import raw as raw_ansi

            table = self.styled_table(border="header")
            for key, desc, _ in group_objects_by_key_and_desc(items, caller=self.caller):
                table.add_row(
                    f"|C{key}|n",
                    "{}|n".format(crop(raw_ansi(desc or ""), width=50) or ""),
                )
            string = f"|wYou are carrying:\n{table}"
        self.msg(text=(string, {"type": "inventory"}))

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
        gear = self.caller.equipment.all()

        table = self.styled_table(border="header")
        for item in gear:
            if item[0] is not None:
                # item_name = item[0].get_display_name()
                item_name, _ = item[0].get_numbered_name(1, self.caller)
                if item[1] in WearLocations:
                    match item[1].value:
                        case "shoulders":
                            equip_str = "around"
                            
                        case _:
                            equip_str = "on"
                            
                    table.add_row(
                        f"<worn {equip_str} {item[1].value}>",
                        f"|C{item_name}|n"
                    )
                else:
                    table.add_row(
                        "<wielded>",
                        f"|C{item_name}|n"
                    )
        string = "|wYour gear:|n"
        
        if not table.get():
            table.add_row("You're not wearing anything.")
            
        string += f"\n{table}"
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
    
class GearCmdSet(CmdSet):
    key = "Main test cmd_set"
    def at_cmdset_creation(self):
        self.add([
                 CmdInventory,
                 CmdEquipment,
                 CmdWear,
                 CmdWield,
                 CmdRemove
             ])
