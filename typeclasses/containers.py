from typeclasses.objects import Object

from evennia.utils import iter_to_str, defaultdict
from utils.utils import iter_to_multiline

class Container(Object):
    appearance_template =  """
{header}
{desc}{characters}{things}
{exits}
{footer}
    """
    
    def at_object_creation(self):
        self.tags.add('container')
        self.tags.add('openable')

        self.db.is_open = False
        self.db.desc_state = f"The {self.get_display_name()} is closed."

    def set_state(self, state_description):
        """
        Sets state descriptions on container.

        Args:
            set_state (str): A state description.

        """
        self.db.desc_state = state_description    
    
    def open(self):
        if not self.db.is_open:
            self.db.is_open = True
            return

    def close(self):
        if self.db.is_open:
            self.db.is_open = False
            return
    
    def get_display_desc(self, looker, **kwargs):
        desc = self.db.desc, self.db.desc_state
        return iter_to_multiline(desc)
    
    def get_display_things(self, looker, **kwargs):
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
        
        out_str = f"|wInside the {self.name}:|n\n {thing_names}"
        
        if not thing_names:
            out_str = f"|wInside the {self.name}:|n\n Nothing but dust."
        
        if self.db.is_open == False:
            out_str = ""
        
        return "\n" + out_str
        
