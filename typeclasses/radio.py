from typeclasses.objects import Object

class Radio(Object):
    def at_object_creation(self):
        self.tags.add('radio')
    pass
