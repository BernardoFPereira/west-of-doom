from commands.command import MuxCommand
from enums import WieldLocations, ObjType
from evennia import CmdSet
# from typeclasses.weapons import Ammo

class ShootCmd(MuxCommand):
    '''
    Fire your equipped[not implemented] weapon at a target.
    Usage:
        shoot <target>
    '''
    help_category = "Combat"
    key = "shoot"
    aliases = ["sh","fire"]

    def func(self):
        if not self.args:
            return self.msg("Shoot what?")
            
        caller = self.caller
        source_room = self.caller.location

        equipped_weapon = [
            eq for eq in caller.equipment.all()
            if eq[0] is not None and (eq[1] == WieldLocations.MAIN_HAND or eq[1] == WieldLocations.TWO_HANDS)
            and eq[0].is_typeclass("typeclasses.weapons.Ranged")
        ]

        if not equipped_weapon:
            caller.msg("Wielding something that can shoot would be helpful.")
            return

        weapon = equipped_weapon[0][0]
        rounds = weapon.contents

        if not rounds:
            caller.msg(f"|wCLICK!|n The {weapon.get_display_name(looker=caller)} is empty!")
            return
        
        shot_noise = weapon.base_weapon_noise + rounds[0].ammo_noise_bonus
        
        target_rooms = source_room.get_rooms_around(source_room.x,
                                                    source_room.y,
                                                    source_room.z,
                                                    shot_noise) #distance
        
        
        for room in target_rooms:
            distance = room[0]
            direction = ''
            
            if source_room.y > room[1].y:
                direction += "north"
            if source_room.y < room[1].y:
                direction += "south"
            
            if source_room.x > room[1].x:
                direction += "east"
            if source_room.x < room[1].x:
                direction += "west"

            if direction:
                direction = f"the {direction}"

            if source_room.z > room[1].z:
                direction = "above"
            if source_room.z < room[1].z:
                direction = "below"
            
            if distance >= 5:
                room[1].msg_contents("|YYou hear the distant thundering of gunfire.|n")
                # room[1].msg_contents(f"|R({source_room} -> {room[1]}) - {distance}|n")
                
            if distance < 5 and distance > 2:
                room[1].msg_contents(f"|yBOOM!|Y Shots fired around {direction}.|n")
                # room[1].msg_contents(f"|R({source_room} -> {room[1]}) - {distance}|n")
                
            if distance > 0 and distance <= 2:
                room[1].msg_contents(f"|yBANG!|Y Shots fired from {direction}.|n", exclude=caller)
                # room[1].msg_contents(f"|R({source_room} -> {room[1]}) - {distance}|n")
                
            if distance == 0:
                room[1].msg_contents("|yBANG!|Y $You() fired a weapon!|n", from_obj=caller)
                room[1].msg_contents(f"Noise: {shot_noise}")
                # room[1].msg_contents(f"|R({source_room} -> {room[1]}) - {distance}|n")

class CmdLoad(MuxCommand):
    key = "load"
    aliases = ["reload", "unload"]

    def func(self):
        caller = self.caller

        equipped_weapon = [
            eq for eq in caller.equipment.all()
            if eq[0] is not None and (eq[1] == WieldLocations.MAIN_HAND or eq[1] == WieldLocations.TWO_HANDS)
        ]

        if not equipped_weapon:
            caller.msg(f"You don't have a firearm to {self.cmdstring}.")
            return
        
        weapon = equipped_weapon[0][0]
        
        rounds_to_load = [
            round for round in caller.contents
            if round.obj_type == ObjType.AMMO and (round.ammo_type == weapon.ammo_type)
        ]
        
        match self.cmdstring:
            case "reload":
                # weapon.unload_weapon(caller)
                caller.msg(f"!! Reloading {weapon}!")
            case "unload":
                if not weapon.contents:
                    caller.msg("Weapon already empty.")
                    return
                
                weapon.unload_weapon(caller)
                caller.msg(f"Unloading {weapon}.")
            case _:
                if rounds_to_load:
                    # Add ammo capacity
                    if len(weapon.contents) == weapon.ammo_capacity:
                        caller.msg("Weapon already full.")
                        return
                        
                    for round in rounds_to_load:
                        if len(weapon.contents) < weapon.ammo_capacity:
                            weapon.load_weapon(round)
                    
                else:
                    caller.msg(f"There's no ammo for your {weapon} left!")
                    return
                
                caller.msg(f"{weapon.name.capitalize()} loaded.")
        pass

class CmdUnload(MuxCommand):
    pass

class CmdReload(MuxCommand):
    pass

class WeaponCommandsCmdSet(CmdSet):
    def at_cmdset_creation(self):
        self.add([ShootCmd, CmdLoad])
