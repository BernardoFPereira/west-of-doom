from commands.command import MuxCommand
from evennia import CmdSet
from evennia import default_cmds

class CmdSay(default_cmds.CmdSay):
    key = "say"
    aliases = ["'", "speak"]

    def func(self):
        if not self.args:
            return self.msg("Say what?")
        
        caller = self.caller
        speech = self.args.strip()
        return caller.location.msg_contents(f"|432$You() $conj(say), '{speech}'|n", from_obj=caller)

class CmdShout(default_cmds.CmdSay, MuxCommand):
    key = "shout"
    aliases = ['"', "yell"]

    def func(self):
        caller = self.caller
        shout = self.args.strip()
        source_room = caller.location
        
        target_rooms = source_room.get_rooms_around(source_room.x,
                                                    source_room.y,
                                                    source_room.z,
                                                    1) #distance
        
        direction = ''

        for room in target_rooms:
            if source_room.y > room[1].y:
                direction += "south"
            if source_room.y < room[1].y:
                direction += "north"

            if source_room.x > room[1].x:
                direction += "east"
            if source_room.x < room[1].x:
                direction += "west"
                
            if source_room.z > room[1].z:
                direction = "above"
            if source_room.z < room[1].z:
                direction = "below"

            if direction != "above" or direction != "below":
                direction = f"the {direction}"

            room[1].msg_contents(f"|425$You() $conj(shout), '{shout}' from {direction}({source_room})!|n"
                                     if room[1] != source_room else 
                                     f"|425$You() $conj(shout), '{shout}'.", from_obj=caller)

class CommunciationCmdSet(CmdSet):
    def at_cmdset_creation(self):
        self.add(CmdSay)
        self.add(CmdShout)