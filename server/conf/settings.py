r"""
Evennia settings file.

The available options are found in the default settings file found
here:

E:\IMPORTANT\Python Workshop\MUD_dev\evenv\Lib\site-packages\evennia\settings_default.py

Remember:

Don't copy more from the default file than you actually intend to
change; this will make sure that you don't overload upstream updates
unnecessarily.

When changing a setting requiring a file system path (like
path/to/actual/file.py), use GAME_DIR and EVENNIA_DIR to reference
your game folder and the Evennia library folders respectively. Python
paths (path.to.module) should be given relative to the game's root
folder (typeclasses.foo) whereas paths within the Evennia library
needs to be given explicitly (evennia.foo).

If you want to share your game dir, including its settings, you can
put secret game- or server-specific settings in secret_settings.py.

"""

# Use the defaults from Evennia unless explicitly overridden
from evennia.settings_default import *

######################################################################
# Evennia base server config
######################################################################

# This is the name of your game. Make it catchy!
SERVERNAME = "West of Doom"
GAME_SLOGAN = "Where you can find the bad, the worse and the terrible!"
SERVER_HOSTNAME = "wot.oriean.space"

# open to the internet: 4000, 4001, 4002
# closed to the internet (internal use): 4005, 4006
TELNET_PORTS = [4000]
WEBSERVER_PORTS = [(4001, 4005)]
WEBSOCKET_CLIENT_PORT = 4002
AMP_PORT = 4006

WEBSOCKET_CLIENT_INTERFACE = '0.0.0.0'

# This needs to be set to your website address for django or you'll receive a
# CSRF error when trying to log on to the web portal
# CSRF_TRUSTED_ORIGINS = ['https://oriean.space']
# ALLOWED_HOSTS = [".oriean.space"]

COMMAND_DEFAULT_CLASS = "commands.command.MuxCommand"
PROTOTYPE_MODULES += [
    "gear.headwear_prototypes",
    "gear.footwear_prototypes",
    "gear.legwear_prototypes",
    "gear.container_prototypes",
    "gear.rifle_prototypes",
    "gear.revolver_prototypes",
    "gear.shotgun_prototypes",
]

CMDSET_UNLOGGEDIN = "evennia.contrib.base_systems.menu_login.UnloggedinCmdSet"
CONNECTION_SCREEN_MODULE = "evennia.contrib.base_systems.menu_login.connection_screens"
AUTO_CREATE_CHARACTER_WITH_ACCOUNT = False

TIME_GAME_EPOCH = 56515968000

TIME_UNITS = {
        "sec": 1,
        "min": 60,
        "hour": 60 * 60,
        "day": 60 * 60 * 24,
        "month": 60 * 60 * 24 * 30,
        "year": 60 * 60 * 24 * 30 * 12,
}


######################################################################
# Settings given in secret_settings.py override those in this file.
######################################################################
try:
    from server.conf.secret_settings import *
except ImportError:
    print("secret_settings.py file not found or failed to import.")
