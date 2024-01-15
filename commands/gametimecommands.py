from evennia.contrib.base_systems import custom_gametime

from commands.command import MuxCommand

class CmdTime(MuxCommand):

    """
    Display the time.

    Usage:
        time

    """

    key = "time"
    locks = "cmd:all()"

    def func(self):
        """Execute the time command."""
        # Get the absolute game time
        year, month, day, hour, mins, secs = custom_gametime.custom_gametime(absolute=True)
        time_string = f"We are in year {year}, day {day}, month {month}."
        time_string += f"\nIt's {hour:02}:{mins:02}:{secs:02}."
        self.msg(time_string)