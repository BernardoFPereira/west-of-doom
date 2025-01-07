from commands.command import MuxCommand
# from typeclasses.rooms import Room
from evennia import CmdSet

class ShootCmd(MuxCommand):
    '''
    Fire your equipped[not implemented] weapon at a target.
    Usage:
        shoot <target>
    '''
    key = "shoot"
    aliases = ["sh","fire","shot"]

    def func(self):
        if not self.args:
            return self.msg("Shoot what?")
            
        caller = self.caller
        source_room = self.caller.location

        target_rooms = source_room.get_rooms_around(source_room.x,
                                                    source_room.y,
                                                    source_room.z,
                                                    8) #distance
        
        
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
                # room[1].msg_contents(f"|R({source_room} -> {room[1]}) - {distance}|n")

class CmdReload(MuxCommand):
    pass

class WeaponCommandsCmdSet(CmdSet):
    def at_cmdset_creation(self):
        self.add(ShootCmd)
