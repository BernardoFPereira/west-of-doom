from evennia import AttributeProperty
from evennia.utils import defaultdict
from typeclasses.objects import Object
from typeclasses.items import Gear
from utils.utils import iter_to_multiline
from enums import ObjType, WieldLocations, AmmoType

# _BARE_HANDS = None

class Weapon(Gear):
    _content_types = ("object",)
    equipment_use_slot = AttributeProperty(WieldLocations.MAIN_HAND)
    weight = AttributeProperty(1)
    
    obj_type = ObjType.WEAPON
    
    # def at_object_creation(self):
        # self.tags.add(['equipment', 'weapon'])

    def get_display_name(self, looker, **kwargs):
        '''
        return object's name, if kwarg are used,
        checks what format it should be.
        '''
            
        display_name = self.key
        
        if kwargs.get("is_dark"):
            display_name = "|hweapon|H"
            
        # if looker:
        #     # Check for Builder permission. If valid, display dbref (#XYZ)
        #     if looker.locks.check_lockstring(looker, "_dummy:perm(Builder)"):
        #         display_name +=  f"({self.dbref})"

        return display_name

    def get_display_things(self, looker, **kwargs):
        if kwargs.get("examination"):
            def _filter_visible(obj_list):
                return (obj for obj in obj_list if obj != looker and obj.access(looker, "view"))

            # sort and handle same-named things
            things = _filter_visible(self.contents_get(content_type="object"))

            grouped_things = defaultdict(list)
            for thing in things:
                grouped_things[thing.get_display_name(looker, **kwargs)].append(thing)

            thing_names = []
            for thingname, thinglist in sorted(grouped_things.items()):
                nthings = len(thinglist)
                thing = thinglist[0]
                singular, plural = thing.get_numbered_name(nthings, looker, key=thingname)
                thing_names.append(singular if nthings == 1 else plural)
            thing_names = iter_to_multiline(thing_names, sep='\n ')
    
            out_str = f"|wLoaded with:|n\n {thing_names}"
    
            if not thing_names:
                out_str = "|nEmpty."
    
            return "\n" + out_str
        return ""
        

    # @property
    # def damage(self):
    #     dmg = self.tags.get(category="damage")
    #     return int(dmg) if isinstance(dmg, str) else None
        
    # @damage.setter
    # def damage(self, damage):
    #     old_dmg = self.tags.get(category="damage")
    #     if old_dmg is not None:
    #         self.tags.remove(old_dmg, category="damage")
    #     if damage is not None:
    #         self.tags.add(str(damage), category="damage")
    
class Ranged(Weapon):
    ammo_type = AttributeProperty(AmmoType.STANDARD)
    ammo_capacity = AttributeProperty(1)
    base_weapon_noise = AttributeProperty(8)

    def at_object_creation(self):
        self.tags.add(['equipment', 'weapon'])

    def load_weapon(self, ammo):
        ammo.location = self

    def unload_weapon(self, holder):
        for ammo in self.contents:
            ammo.location = holder
    
    # @property
    # def is_loaded(self):
    #     ammo = self.tags.get(category="ammo_capacity")
    #     return ammo

    # @ammo_capacity.setter
    # def ammo_capacity(self, ammo_capacity):
    #     old_clip = self.tags.get(category="ammo_capacity")
    #     if old_clip is not None:
    #         self.tags.remove(old_clip, category="ammo_capacity")
    #     if ammo_capacity is not None:
    #         self.tags.add(str(ammo_capacity), category="ammo_capacity")

class Ammo(Object):
    damage = AttributeProperty(1)
    ammo_type = AttributeProperty(AmmoType.STANDARD)
    ammo_noise_bonus = AttributeProperty(0)
    obj_type = ObjType.AMMO

    def at_pre_impact(self, target):
        pass

    def at_post_impact(self, target):
        pass

    def get_display_name(self, looker, **kwargs):
        '''
        return object's name, if kwarg are used,
        checks what format it should be.
        '''
            
        display_name = self.key 

        match self.ammo_type:
            case AmmoType.SHELLS:
                display_name = f"shotgun {self.key}"
                pass
            # case AmmoType.ARROW:
            #     pass
            # case AmmoType.BOLT:
            #     pass
            case _:
                pass
        
        if kwargs.get("is_dark"):
            display_name = "|hmunition|n"
            
        # if looker:
        #     # Check for Builder permission. If valid, display dbref (#XYZ)
        #     if looker.locks.check_lockstring(looker, "_dummy:perm(Builder)"):
        #         display_name +=  f"({self.dbref})"

        return display_name
# class BareHands(Weapon):
#     obj_type = ObjType.WEAPON
#     equipment_use_slot = WieldLocations.MAIN_HAND

# def get_bare_hands():
#     global _BARE_HANDS
#     if not _BARE_HANDS:
#         _BARE_HANDS = search
