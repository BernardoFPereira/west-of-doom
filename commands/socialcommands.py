import evennia
from evennia.utils import inherits_from
from commands.command import MuxCommand
from evennia import CmdSet

class CmdSocialNod(MuxCommand):
    '''
    |BSocial emote.|n
    The best way to agree in silence.

    Usage:
        nod
        nod <someone>
    '''
    help_category = 'Social Emotes'
    key = 'nod'

    def parse(self):
        args = self.args.strip()
        if not args:
            self.target = ""
        else:
            self.target = args

    def func(self):
        caller = self.caller
        # Check to see if a target was specified
        if not self.target:
            self.msg(f"|520You nod solemnly.|n")
            self.caller.location.msg_contents(
                f"|520$You(self) $conj(nod) solemnly.|n",
                exclude=self.caller,
                mapping={'self':self.caller.get_display_name()})
            return
        # Check if the target was 'self' or caller name
        if (self.target.lower() == 'self') or (self.target.lower() == self.caller.key.lower()):
            self.msg(f'|520You nod to yourself.|n')
            self.caller.location.msg_contents(
                f"|520$You(caller) $conj(nod) to $pron(yourself,{self.caller.db.gender}).|n",
                exclude=self.caller,
                mapping={'caller':self.caller.get_display_name()})
            return
        # Look for corresponding object in location
        target = caller.search(self.target, candidates=caller.location.contents)
                            #    typeclass=['typeclasses.characters.Character','typeclasses.mounts.Mount'],quiet=True)
        # If specified target is not found in location, terminate
        if target.is_typeclass('typeclasses.characters.Character'):
            target = target

        if not target:
            self.msg('No one by that name here.')
            return
        # Check if specified target is not the same as command caller
        if target.key != self.caller.key:
            self.msg(f"|520You nod in agreement with {target.get_display_name()}.|n")
            self.caller.location.msg_contents(
                f"|520$You(caller) $conj(nod) in agreement with $you(target).|n",
                exclude=[self.caller, target],
                mapping={'caller':self.caller.get_display_name(),
                        'target':target.get_display_name()}
                )
            self.caller.location.msg_contents(
                f"|520$You(caller) $conj(nod) in agreement with you.|n",
                exclude=[obj for obj in self.caller.location.contents if obj.key != target.key],
                mapping={'caller':self.caller.get_display_name()}
                )
            return
        self.msg(f"|520You nod solemnly.|n")

class CmdSocialShake(MuxCommand):
    '''
    |BSocial emote.|n
    The best way to disagree in silence.

    Usage:
        shake
        shake <someone>
    '''
    help_category = 'Social Emotes'
    key = 'shake'

    def parse(self):
        args = self.args.strip()
        if not args:
            self.target = ""
        else:
            self.target = args

    def func(self):
        caller = self.caller
        # Check to see if a target was specified
        if not self.target:
            self.msg(f"|520You shake your head.|n")
            caller.location.msg_contents(
                f"|520$You(caller) $conj(shake) $pron(your,{self.caller.db.gender}) head.|n",
                exclude=caller,
                mapping={'caller':caller.get_display_name()})
            return
        # Look for corresponding object in location
        target = caller.search(self.target, candidates=caller.location.contents,
                               typeclass=['typeclasses.characters.Character','typeclasses.mounts.Mount'],quiet=True)
        # If specified target is not found in location, terminate
        if not target:
            target = caller.search(self.target, candidates=caller.location.contents,quiet=True)
            if inherits_from(target, 'typeclasses.animals.Animal'):
                target = target
            if not target:
                self.msg('No one by that name here.')
                return
        # Check if specified target is not the same as command caller
        if target[0].key != caller.key:
            # Self msg
            self.msg(f"|520You shake your head in disagreement with {target[0].get_display_name()}.|n")
            # Onlookers msg
            caller.location.msg_contents(
                f"|520$You(caller) $conj(shake) $pron(your,{caller.db.gender}) head in disagreement with $you(target).|n",
                exclude=[caller, target[0]],
                mapping={'caller':caller.get_display_name(),
                         'target':target[0].get_display_name()}
                )
            # Target msg
            self.caller.location.msg_contents(
                f"|520$You(caller) $conj(shake) $pron(your,{self.caller.db.gender}) head in disagreement with you.|n",
                exclude=[obj for obj in self.caller.location.contents if obj.key != target[0].key],
                mapping={'caller':self.caller.get_display_name()}
                )
            return

        self.msg(f'|520You shake your head.|n')

class CmdSocialPat(MuxCommand):
    '''
    |BSocial emote.|n
    Pat pat.
    
    Usage:
        pat
        pat <someone>
    '''
    key = 'pat'

    def parse(self):
        super().parse()
        
    def func(self):
        self.msg(f"Pat pat!")
    

class CmdSocialSmile(MuxCommand):
    '''
    |BSocial emote.|n
    It's great to be in here! Smile!

    Usage:
        smile
        smile <someone>
    '''
    help_category = 'Social Emotes'
    key = 'smile'

    def parse(self):
        args = self.args.strip()
        if not args:
            self.target = ""
        else:
            self.target = args

    def func(self):
        caller = self.caller
        # Check to see if a target was specified
        if not self.target:
            self.msg(f'|520You smile happily.|n')
            caller.location.msg_contents(
                f'|520$You(caller) $conj(smile) happily.|n',
                exclude=caller,
                mapping={'caller':caller.get_display_name()})
            return
        # Look for corresponding object in location
        target = caller.search(self.target, candidates=caller.location.contents,
                               typeclass=['typeclasses.characters.Character','typeclasses.mounts.Mount'],quiet=True)
        # If specified target is not found in location, terminate
        if not target:
            target = caller.search(self.target, candidates=caller.location.contents,quiet=True)
            if inherits_from(target, 'typeclasses.animals.Animal'):
                target = target
            if not target:
                self.msg('No one by that name here.')
                return
        # Check if specified target is not the same as command caller
        if target[0].key != caller.key:
            self.msg(f"|520You smile at {target[0].get_display_name()}|520.|n")
            target[0].msg(f"|520{caller.get_display_name()} smiles at you.|n")
            caller.location.msg_contents(
                f'|520$You(caller) $conj(smile) at $You(target).|n',
                exclude=[caller,target[0]],
                mapping={'caller':caller.get_display_name(),
                         'target':target[0].get_display_name()}
                         )

            return
        self.msg(f'|520You smile happily.|n')

class CmdSocialRoar(MuxCommand):
    '''
    |BSocial emote.|n
    Rage! RAGE!
    '''
    help_category = 'Social Emotes'
    key = 'roar'

    def func(self):
        self.caller.location.msg_contents(f'|520$You(caller) roars angrily.|n',
                                            exclude=self.caller,
                                            mapping={'caller':self.caller.get_display_name()})
        self.msg(f'|520You roar angrily.|n')

class CmdSocialCheer(MuxCommand):
    '''
    |BSocial emote.|n
    Take part in the gleeful side of life.
    Cheer!
    '''
    help_category = 'Social Emotes'
    key = 'cheer'
    
    def parse(self):
        args = self.args.strip()
        if not args:
            self.target = ""
        else:
            self.target = args

    def func(self):
        caller = self.caller
        # Check to see if a target was specified
        if not self.target:
            self.msg(f"|520You raise your arms, cheering! Hooray!|n")
            self.caller.location.msg_contents(
                f'|520$You(caller) raises $pron(your,{self.caller.db.gender}) arms, cheering!|n',
                exclude=self.caller,
                mapping={'caller':self.caller.get_display_name()}
                )
            return
        target = caller.search(self.target, candidates=caller.location.contents, typeclass=['typeclasses.characters.Character','typeclasses.mounts.Mount'],quiet=True)
        # If specified target is not found in location, terminate
        if not target:
            target = caller.search(self.target, candidates=caller.location.contents,quiet=True)
            if inherits_from(target, 'typeclasses.animals.Animal'):
                target = target
            if not target:
                self.msg('No one by that name here.')
                return
        # Check if specified target is not the same as command caller
        if target[0].key != self.caller.key:
            self.caller.location.msg_contents(
                f"|520You cheer for $pron(your,{target[0].db.gender}) succes!|n",
                exclude = [obj for obj in target if obj.key != self.caller.key],

                )
            target[0].msg(f"|520{self.caller.get_display_name()} cheers for your success!")
            self.caller.location.msg_contents(
                f"|520$You(caller) cheers for $you(target)'s success!|n",
                exclude=[self.caller,target[0]],
                mapping={'caller':self.caller.get_display_name(),
                         'target':target[0].get_display_name()})
            return
        self.msg(f'|520You raise your arms, cheering! Hooray!|n')

class CmdSocialBow(MuxCommand):
    '''
    |BSocial emote.|n
    Respectfully greet your fellow players.

    Usage:
        bow
        bow <someone>
    '''
    help_category = 'Social Emotes'

    key = 'bow'

    def parse(self):
        args = self.args.strip()
        if not args:
            self.target = ""
        else:
            self.target = args

    def func(self):
        # Check to see if a target was specified
        if not self.target:
            self.msg(f'|520You bow deeply.|n')
            self.caller.location.msg_contents(
                f'|520$You(caller) bows deeply.|n',
                exclude=self.caller,
                mapping={'caller':self.caller.get_display_name()}
                )
            return
        # Look for corresponding object in location
        target = self.caller.search(self.target, typeclass='typeclasses.characters.Character', quiet=True)
        # If specified target is not found in location, terminate
        if not target:
            self.msg(f"No one by that name around...")
            return
        # Check if specified target is not the same as command caller
        if target[0].key != self.caller.key:
            self.msg(f"|520You bow before {target[0].get_display_name()}|520.|n")

            target[0].msg(f"|520{self.caller.get_display_name()} bows before you.|n")

            self.caller.location.msg_contents(f"|520$You(caller) bows before $you(target).|n",
                                                exclude=[self.caller,target[0]],
                                                mapping={'caller':self.caller.get_display_name(),
                                                         'target':target[0].get_display_name()})
            return

        self.msg(f'|520You bow deeply.|n')

class CmdSocialSit(MuxCommand):
    '''
    Sit down.

    Usage:
        sit
    '''
    key = 'sit'

    def func(self):
        # Check caller stance
        if self.caller.db.stance:
            # if already sitting - bail
            if self.caller.db.stance == 'sitting':
                self.msg("You're already sitting!")
                return
            # if not - sit
            self.caller.db.stance = 'sitting'

        # Send emote announcement to location
        self.caller.location.msg_contents(
            f"$You(caller) $conj(sit) down.",
            exclude=self.caller,
            mapping={'caller':self.caller.get_display_name()}
            )
        # And to self
        self.msg("You sit down.")

class CmdSocialStand(MuxCommand):
    '''
    Stand up.

    Usage:
        stand
    '''
    key = 'stand'

    def func(self):
        # Check caller stance
        if self.caller.db.stance:
            # if already standing - bail
            if self.caller.db.stance == 'standing':
                self.msg("You're already standing!")
                return
            # if not - stand
            self.caller.db.stance = 'standing'

        # Send emote announcement to location
        self.caller.location.msg_contents(
            f"$You(caller) $conj(stand) up.",
            exclude=self.caller,
            mapping={'caller':self.caller.get_display_name()}
            )
        # And to self
        self.msg("You stand up.")

# TODO More social emotes for the collection.
class SocialCmdSet(CmdSet):
    key = 'SocialEmotes'

    def at_cmdset_creation(self):
        self.add(CmdSocialNod)
        self.add(CmdSocialBow)
        self.add(CmdSocialShake)
        self.add(CmdSocialSmile)
        self.add(CmdSocialRoar)
        self.add(CmdSocialCheer)
        self.add(CmdSocialSit)
        self.add(CmdSocialStand)
        self.add(CmdSocialPat)
