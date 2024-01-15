from commands.command import MuxCommand
from evennia import CmdSet
from typeclasses.characters import Character
from evennia import search_tag

class CmdRadio(MuxCommand):
    '''
    If you want to communicate over long distances you'll
    usually need more than your lungs!
    In our case, we use |Gradios|n.

    As long as you are carrying or otherwise with access to
    any |wradio|n item, you can transmit messages over long
    distances. The recipient of the message must also have
    a working radio with them, if not they'll be shown as
    unreachable.

    Usage:
        radio <target> <message>

    See also:
    BROADCAST
    '''

    key = 'radio'

    def parse(self):
        self.args = self.args.strip()
        target, *message = self.args.split(' ', 1)
        self.target = target.strip()

        if not message:
            self.message = ""
        else:
            self.message = message[0]

    def func(self):
        radioes = search_tag('radio')
        caller = self.caller
        
        for item in radioes:
            if item in caller.contents:
                if not self.message:
                    caller.msg(f"You fidget with your {item.name}, mindlessly.")
                    caller.location.msg_contents(
                        f"|h$You()|H $conj(fidget) with $pron(your,{caller.db.gender[0]}) $obj(item), midlessly.",
                        exclude=caller,
                        from_obj=caller,
                        mapping={'item':item}
                        )
                    return
                target = caller.search(self.target, typeclass="typeclasses.characters.Character", global_search=True, quiet=True)
                if not target:
                    self.msg(f"You can't reach anyone by that name...")
                    return
                if target[0] == caller:
                    self.msg("You can't radio yourself!")
                    return
                if not self.message:
                    self.msg("They'll never hear you if you don't say anything.")
                    return
                for item in radioes:
                    if item in target[0].contents and target[0].has_account:
                        self.msg(f"|YYou transmit to |y{target[0].key}|Y '{self.message}'|n")
                        target[0].msg(f"|y{caller.key}|Y transmits '{self.message}'|n")
                        return
                self.msg(f"|y{target[0].key}|Y is currently unreachable.|n")
                return
        self.msg("How? You don't have a working radio!")

class CmdBroadcast(MuxCommand):
    '''
    If you want to communicate over long distances you'll
    usually need more than your lungs!
    In our case, we use |Gradios|n.

    As long as you are carrying or otherwise with access to
    any |wradio|n item, you can transmit messages over long
    distances. Aside from |Yradio|ning specific people, you
    can |Ybroadcast|n a message globally for everyone with
    a working radio.

    Usage:
        broadcast <message>
    
    See also:
    RADIO
    '''

    key = 'broadcast'
    aliases = ['cast']

    def parse(self):
        message = self.args.strip()
        if not message:
            self.message = ""
        else:
            self.message = message

    def func(self):
        radioes = search_tag('radio')
        caller = self.caller

        for item in radioes:
            if item in caller.contents:
                if not self.message:
                    caller.msg(f"You fidget with your {item.name}, mindlessly.")
                    caller.location.msg_contents(
                        f"$You() $conj(fidget) with $pron(your,{caller.db.gender[0]}) $obj(item), mindlessly.",
                        exclude=caller,
                        from_obj=caller,
                        mapping={'item':item}
                        )
                    return
                chars = Character.objects.all()
                targets = [obj for obj in chars if (obj.has_account and obj != caller)]
                for target in targets:
                    for item in radioes:
                        if item in target.contents:
                            item.location.msg(f"|521{caller.get_display_name()} broadcasts '{self.message}'|n")
                self.msg(f"|521You broadcast '{self.message}'|n")
                return
        self.msg("How? You don't have a working radio!")

class RadioCmdSet(CmdSet):

    key = 'RadioCommunication'

    def at_cmdset_creation(self):
        self.add(CmdRadio)
        self.add(CmdBroadcast)