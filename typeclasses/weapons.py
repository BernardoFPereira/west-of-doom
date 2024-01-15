from typeclasses.objects import Object

class Weapon(Object):
    def at_object_creation(self):
        self.tags.add(['equipment', 'weapon'])
        
    @property
    def damage(self):
        dmg = self.tags.get(category="damage")
        return int(dmg) if isinstance(dmg, str) else None
        
    @damage.setter
    def damage(self, damage):
        old_dmg = self.tags.get(category="damage")
        if old_dmg is not None:
            self.tags.remove(old_dmg, category="damage")
        if damage is not None:
            self.tags.add(str(damage), category="damage")
    
class Ranged(Weapon):
    @property
    def ammo_clip(self):
        ammo = self.tags.get(category="ammo_clip")
        return ammo

    @ammo_clip.setter
    def ammo_clip(self, ammo_clip):
        old_clip = self.tags.get(category="ammo_clip")
        if old_clip is not None:
            self.tags.remove(old_clip, category="ammo_clip")
        if ammo_clip is not None:
            self.tags.add(str(ammo_clip), category="ammo_clip")

