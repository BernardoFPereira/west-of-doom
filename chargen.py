from typeclasses.characters import Character
from random_tables import chargen_tables
from rules import dice

_TEMP_SHEET = """
{name}

BOD: {body}
MND: {mind}
GRT: {grit}
REF: {reflex}
CUN: {cunning}

{description}

"""

class TemporaryCharacterSheet:
    def _random_ability(self):
        return min(dice.roll("1d6"), dice.roll("1d6"), dice.roll("1d6"))

    def __init__(self):
        self.body = self._random_ability()
        self.mind = self._random_ability()
        self.grit = self._random_ability()
        self.reflex = self._random_ability()
        self.cunning = self._random_ability()

        physique = dice.roll_random_table('1d20', chargen_tables['physique'])
        face = dice.roll_random_table('1d20', chargen_tables['face'])
        skin = dice.roll_random_table('1d20', chargen_tables['skin'])
        hair = dice.roll_random_table('1d20', chargen_tables['hair'])

        self.desc = (
            f"You are {physique} with a {face}, {skin} skin, {hair} hair."
        )

        self.hp_max = 100
        self.hp = self.hp_max
        self.xp = 0
        self.level = 1

    def show_sheet(self):
        return _TEMP_SHEET.format(
            name = self.name,
            body = self.body,
            grit = self.grit,
            reflex = self.reflex,
            cunning = self.cunning,
            description = self.desc
        )
