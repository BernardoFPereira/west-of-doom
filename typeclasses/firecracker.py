from typeclasses.objects import Object

class Firecracker(Object):
    def at_get(self, getter):
        getter.msg(f'Watch out {self.key} might explode!')
