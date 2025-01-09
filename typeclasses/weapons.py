from typeclasses.objects import Object

class Weapon(Object):
    
    _content_types = ("object",)
    
    def at_object_creation(self):
        self.tags.add(['equipment', 'weapon'])

    def get_display_name(self, looker, **kwargs):
        '''
        return object's name, if kwarg are used,
        checks what format it should be.
        '''
            
        display_name = f"|h{self.key}|H" 
        
        if kwargs.get("is_dark"):
            display_name = "|hweapon|H"
            
        # if looker:
        #     # Check for Builder permission. If valid, display dbref (#XYZ)
        #     if looker.locks.check_lockstring(looker, "_dummy:perm(Builder)"):
        #         display_name +=  f"({self.dbref})"

        return display_name

        
        
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

