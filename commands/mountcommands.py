from commands.command import MuxCommand
from evennia import CmdSet
from typeclasses.mounts import Mount

class CmdRide(MuxCommand):
    '''
    Take an animal as your mount and start |wriding|n it.
    Only usable in available mounts.

    You'll automatically |wride|n a mount being led by you.

    Usage:
        ride <mount>
        ride
    '''
    help_category = 'Mounts/Riding'
    key = 'ride'

    def parse(self):
        self.args = self.args.strip()
        if not self.args:
            self.target = ''
        else:
            self.target = self.args
    
    def func(self):

        if not self.target:
            if not self.caller.ndb.mount:
                return self.msg('Ride what?')

            if self.caller.ndb.is_riding:
                return self.msg(get_is_riding_error(self.caller))
            
            self.caller.ndb.is_riding = True
            self.caller.ndb.mount.ndb.is_ridden = True
            self.caller.ndb.mount.tags.add('ridden_mount')

        else:
            if self.caller.ndb.is_riding:
                return self.msg(get_is_riding_error(self.caller))
            
            target_mount = self.caller.search(self.target, quiet=True)
            
            if not target_mount:
                return self.msg(f"There's no {self.args} around that you can ride.")
            
            target_mount = target_mount[0]

            if not target_mount.is_typeclass(Mount):
                return self.msg("You can't ride that!")
            
            if self.caller.ndb.mount:
                if target_mount != self.caller.ndb.mount:
                    return self.msg(f"That's not your mount!1")
            
            if target_mount.ndb.rider:
                if self.caller != target_mount.ndb.rider:
                    return self.msg(f"That's not your mount!2")

            target_mount.ndb.rider = self.caller
            self.caller.ndb.mount = target_mount

            target_mount.ndb.is_ridden = True
            self.caller.ndb.is_riding = True
            
            target_mount.tags.add('ridden_mount')

        self.caller.location.msg_contents(f'$You() $conj(start) riding {self.caller.ndb.mount.get_display_name()}.', from_obj=self.caller)
    
class CmdLead(MuxCommand):
    '''
    Take an animal as you mount without |wriding|n it.
    Only usable in an available mount.

    You'll automatically |wlead|n a mount you're |wriding|n.
    
    Usage:
        lead <mount>
        lead
    '''
    help_category = 'Mounts/Riding'
    key = 'lead'
    
    def parse(self):
        self.args = self.args.strip()
        if not self.args:
            self.target = ''
        else:
            self.target = self.args
    
    def func(self):
        target_mount = self.caller.search(self.target, quiet=True)
        out_string = ''

        if not target_mount:
            if not self.caller.ndb.mount:
                self.caller.msg('Lead what?')
                return
            
            mount_cap_name = self.caller.ndb.mount.get_display_name()[0].upper() + self.caller.ndb.mount.get_display_name()[1:]
            out_string = f"{mount_cap_name} is already following you!"
            
        if self.caller.ndb.is_riding:
            CmdDismount.func(self, lead=True)
            out_string = f"$You() $conj(start) leading {self.caller.ndb.mount.get_display_name()}."

        else:    
            mount_cap_name = target_mount[0].get_display_name()[0].upper() + target_mount[0].get_display_name()[1:]
            
            if not target_mount[0].is_typeclass(Mount):
                return self.msg("You may only lead mounts!")  
                      
            if target_mount[0].ndb.rider:
                if target_mount[0].ndb.rider != self.caller:
                    return self.msg(f"That's not your mount!")

            if self.caller.ndb.mount and target_mount[0] != self.caller.ndb.mount:
                if self.caller.ndb.is_riding:
                    return self.msg(get_is_riding_error(self.caller))
                CmdAbandon.func(self)

            if target_mount[0] == self.caller.ndb.mount and not self.caller.ndb.is_riding:
                return self.msg(f'{mount_cap_name} is already following you!')

            if target_mount[0] == self.caller.ndb.mount and self.caller.ndb.is_riding:
                CmdDismount.func(self, lead=True)

            out_string = f"$You() $conj(start) leading {target_mount[0].get_display_name()}."

            self.caller.ndb.mount = target_mount[0]
            target_mount[0].ndb.rider = self.caller
                
        self.caller.location.msg_contents(out_string, from_obj=self.caller)
        

class CmdDismount(MuxCommand):
    '''
    Leave the back of your trusty mount and start |wleading|n it.

    Usage:
        dismount
    '''
    help_category = 'Mounts/Riding'
    key = 'dismount'

    def func(self, lead=False):
        mount = self.caller.ndb.mount

        if not mount:
            self.msg("You have no mount!")
            return
        
        if not self.caller.ndb.is_riding:
            self.msg("You're not even riding!")
            return

        del self.caller.ndb.is_riding
        del mount.ndb.is_ridden

        if lead:
            self.caller.location.msg_contents(f"$You() $conj(dismount) from {mount.get_display_name()}, and stops riding.", from_obj=self.caller)
            mount.tags.remove('ridden_mount')
            return

        del self.caller.ndb.mount
        del mount.ndb.rider
        
        self.caller.location.msg_contents(f"$You() $conj(dismount) from {mount.get_display_name()}, and stops riding.", from_obj=self.caller)
        mount.tags.remove('ridden_mount')

class CmdAbandon(MuxCommand):
    '''
    Makes a mount you are |wleading|n stop following you.

    Usage:
        abandon
    '''

    help_category = 'Mounts/Riding'    
    key = 'abandon'

    def func(self):
        mount = self.caller.ndb.mount
        
        if not mount:
            self.msg('You have no mount!')
            return
        
        if self.caller.ndb.is_riding:
            self.msg("You can't abandon a mount while riding it!")
            return
        
        mount_cap_name = mount.get_display_name()[0].upper() + mount.get_display_name()[1:]

        del self.caller.ndb.mount
        del mount.ndb.rider

        self.msg(f'{mount_cap_name} will no longer follow you.')


class MountCmdSet(CmdSet):
    key = 'MountInteraction'

    def at_cmdset_creation(self):
        self.add(CmdRide)
        self.add(CmdDismount)
        self.add(CmdLead)
        self.add(CmdAbandon)

def get_is_riding_error(caller):
    return f"You're already riding {caller.ndb.mount.get_display_name()}!"
