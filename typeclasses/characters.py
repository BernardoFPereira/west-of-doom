"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""
import random
from evennia.objects.objects import DefaultCharacter
from .objects import ObjectParent
from django.utils.translation import gettext as _
from rules import dice

class LivingMixin:
    is_pc = False
    
    @property
    def hurt_level(self):
        """
        String describing how hurt this character is.
        """
        
        percent = max(0, min(100, 100 * (self.hp / self.hp_max)))
        if 95 < percent <= 100:
            return "|gUnharmed|n"
        elif 80 < percent <= 95:
            return "|gScraped|n"
        elif 60 < percent <= 80:
            return "|GBruised|n"
        elif 45 < percent <= 60:
            return "|yHurt|n"
        elif 30 < percent <= 45:
            return "|yWounded|n"
        elif 15 < percent <= 30:
            return "|rBadly wounded|n"
        elif 1 < percent < 15:
            return "|rBarely hanging on|n"
        elif percent == 0:
            return "|RCollapsed!|n"

    def heal(self, hp):
        """
        Heal hp amount of health, not allowing to exceed our max hp
        """
        damage = self.hp_max - self.hp
        healed = min(damage, hp)
        self.hp += healed

        self.msg(f"You heal for {healed} HP.")

    def at_attacked(self, attacker, **kwargs):
        """
        Called when being attacked and combat starts
        """
        pass

    def at_damage(self, damage, attacker=None):
        """Called when attacked and taking damage"""
        self.hp -= damage

    def at_defeat(self):
        """
        Called when defeated. By default this means death
        """
        self.at_death()

    def at_death(self):
        """Called when this thing dies."""
        # this will mean different things for different living things
        pass

    def at_do_loot(self, looted):
        looted.at_looted(self)

    def at_looted(self, looter):
        """Called when looted by another entity"""

        # default to stealing some coins
        max_steal = dice.roll("1d10")
        stolen = self.at_pay(max_steal)
        looter.coins += stolen

    def at_pay(self, amount):
        """When paying coins, make sure to never detract more than we have"""
        amount = min(amount, self.coins)
        self.coins -= amount
        return amount
    
    
class Character(ObjectParent, LivingMixin, DefaultCharacter):
    """
    The Character defaults to reimplementing some of base Object's hook methods with the
    following functionality:

    at_basetype_setup - always assigns the DefaultCmdSet to this object type
                    (important!)sets locks so character cannot be picked up
                    and its commands only be called by itself, not anyone else.
                    (to change things, use at_object_creation() instead).
    at_post_move(source_location) - Launches the "look" command after every move.
    at_post_unpuppet(account) -  when Account disconnects from the Character, we
                    store the current location in the pre_logout_location Attribute and
                    move it to a None-location so the "unpuppeted" character
                    object does not need to stay on grid. Echoes "Account has disconnected"
                    to the room.
    at_pre_puppet - Just before Account re-connects, retrieves the character's
                    pre_logout_location Attribute and move it back on the grid.
    at_post_puppet - Echoes "AccountName has entered the game" to the room.

    """
    
    appearance_template =  """
{header}
|y{name}|n
{desc}{characters}{things}
{exits}
{footer}
    """

    is_pc = True

    def at_object_creation(self):
        self.db.gender = 'male'
        self.db.stance = 'standing'

        self.db.strength = random.randint(6,20)
        self.db.dexterity = random.randint(6,20)
        self.db.intelligence = random.randint(6,20)

    @property
    def prompt(self):
        location = self.location
        prompt_sep = " "

        prompt_room_info = "{light}{terrain}".format(light = 'o' if location.db.is_dark else '*',
                                                     terrain = location.db.terrain_str)
        
        prompt_char_stats = "{ride}{sneak}{swim}".format(ride = 'R' if self.ndb.is_riding else "",
                                                         sneak = 'S' if self.ndb.sneaking else "",
                                                         swim = 'W' if self.db.will_swim else "",
                                                         )
        prompt_ending = ">\n"

        prompt = prompt_room_info + prompt_sep + prompt_char_stats + prompt_sep + prompt_ending
        if not prompt_char_stats:
            prompt = prompt_room_info + prompt_sep + prompt_ending

        return prompt

    @property
    def stats(self):
        string = """
        STR: {}, DEX: {}, INT: {}
        """.format( self.db.strength, self.db.dexterity, self.db.intelligence)

        return string
    
    # def get_stats(self):
    #     '''
    #     Get the main stats of this character
    #     '''
    #     return self.db.strength, self.db.dexterity, self.db.intelligence

    def get_gender(self):
        '''
        Get the gender of this character
        '''
        return self.db.gender

    def get_display_name(self, looker=None, **kwargs):
        '''
        return object's name, if kwarg are used,
        checks what format it should be.
        '''
        display_name = f"|h{self.key.capitalize()}|H"
        if looker:
            # Check for Builder permission. If valid, display dbref (#XYZ)
            if looker.locks.check_lockstring(looker, "_dummy:perm(Builder)"):
                display_name +=  f"({self.dbref})"
        return display_name

    def at_pre_move(self, destination, move_type="move", **kwargs):
        if self.db.stance != 'standing':
            return False
        return super().at_pre_move(destination, move_type, **kwargs)

    def at_post_move(self, source_location, move_type="move", **kwargs):
        if self.ndb.is_riding:
            self.ndb.mount.move_to(self.location, move_type="follow")
        super().at_post_move(source_location, move_type)
        if not self.ndb.riding and self.ndb.mount:
            self.ndb.mount.move_to(self.location, move_type="follow")
        if self.ndb.followers:
            self.ndb.followers.move_to(self.location, move_type="follow")

    def announce_move_from(self, destination, msg=None, mapping=None, move_type="move", **kwargs):
        if not self.location:
            return
        if msg:
            string = msg
        else:
            string = "|234{object} leaves {exit}.|n"
            if self.ndb.is_riding:
                string = "|234{object} leaves {exit}, " + f"riding {self.ndb.mount.get_display_name()}.|n"

        location = self.location
        exits = [
            o for o in location.contents if o.location is location and o.destination is destination
        ]
        if not mapping:
            mapping = {}

        mapping.update(
            {
                "object": self.get_display_name() if self.is_typeclass(Character,exact=True) else (self.get_display_name()[0].upper() + self.get_display_name()[1:]),
                "exit": exits[0].name if exits else "somewhere",
                "origin": location or "nowhere",
                "destination": destination or "nowhere",
            }
        )

        location.msg_contents(
            (string, {"type": move_type}), exclude=(self,), from_obj=self, mapping=mapping
        )

    def announce_move_to(self, source_location, msg=None, mapping=None, move_type="move", **kwargs):
        if not source_location and self.location.has_account:
            # This was created from nowhere and added to an account's
            # inventory; it's probably the result of a create command.
            string = _("You now have {name} in your possession.").format(
                name=self.get_display_name(self.location)
            )
            self.location.msg(string)
            return

        if source_location:
            if msg:
                string = msg
            else:
                string = _("|233{object} has arrived from {exit}.|n")
                if self.ndb.is_riding:
                    string = _("|233{object} has arrived from {exit}, " + f"riding {self.ndb.mount.get_display_name()}.|n")
        else:
            string = _("|233{object} has suddenly arrived.|n")

        origin = source_location
        destination = self.location
        exits = []
        if origin:
            exits = [
                o for o in destination.contents
                if o.location is destination and o.destination is origin
            ]

        if not mapping:
            mapping = {}

        mapping.update(
            {
                "object": self.get_display_name(),
                "exit": ('below' if exits[0].name == 'down' else 'above' if exits[0].name == 'up' else f"the {exits[0].name}") if exits else "somewhere",
                "origin": origin or "nowhere",
                "destination": destination or "nowhere",
            }
        )

        destination.msg_contents(
            (string, {"type": move_type}), exclude=(self,), from_obj=self, mapping=mapping
        )

    def at_post_puppet(self, **kwargs):
        """
        Called just after puppeting has been completed and all
        Account<->Object links have been established.

        Args:
            **kwargs (dict): Arbitrary, optional arguments for users
                overriding the call (unused by default).
        Note:
            You can use `self.account` and `self.sessions.get()` to get
            account and sessions at this point; the last entry in the
            list from `self.sessions.get()` is the latest Session
            puppeting this Object.

        """
        self.msg(_("\nYou become |c{name}|n.\n").format(name=self.key))
        self.msg((self.at_look(self.location), {"type": "look"}), options=None)
    
        def message(obj, from_obj):
            obj.msg(
                _("{name} has entered the game.").format(name=self.get_display_name(obj)),
                from_obj=from_obj,
            )

        self.location.for_contents(message, exclude=[self], from_obj=self)

    def at_post_unpuppet(self, account=None, session=None, **kwargs):
        if self.ndb.mount:
            if self.ndb.is_riding:
                self.execute_cmd("dismount")
            self.execute_cmd("abandon")

        return super().at_post_unpuppet(account, session, **kwargs)

