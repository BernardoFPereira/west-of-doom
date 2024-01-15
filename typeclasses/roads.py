# from typeclasses.exits import Exit

# class Road(Exit):

#     def at_object_creation(self):        
#         self.db.desc = "This is a 'roads.X' object."
#         self.db.road_name = 'road'

#     def get_display_name(self, looker=None, **kwargs):
      
#         display_name = f"={self.name}="
#         # Check for Builder permission. If valid, display dbref (#XYZ)
#         return (display_name + f"({self.dbref})" if looker.locks.check_lockstring(looker, "_dummy:perm(Builder)") else display_name)

# class Trail(Exit):

#     def at_object_creation(self):
#         self.db.road_name = 'trail'

#     def get_display_name(self, looker=None, **kwargs):
      
#         display_name = f"-{self.name}-"
#         # Check for Builder permission. If valid, display dbref (#XYZ)
#         return (display_name + f"({self.dbref})" if looker.locks.check_lockstring(looker, "_dummy:perm(Builder)") else display_name)