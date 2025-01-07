from evennia.utils import make_iter

def iter_to_multiline(iterable, sep="\n"):
    """
    This formats an iterable list as multi-line string output.

    Args:
        iterable (any): Usually an iterable to print. Each element must be possible to
            present with a string.
            Note that if this is a generator, it will be consumed by this operation.

        sep (str): The string to create a new line for each item in the iterable.

    Returns:
        str: The list represented as a multi-line string.

    Examples:

        ```python
        >>> iter_to_multiline([1,2,3])
        1
        2
        3
        ```
    """
    iterable = list(make_iter(iterable))
    if not iterable:
        return

    return f"{sep}".join(str(item) for item in iterable).strip()

def capitalize_name(obj, looker):
    """
    Simple function to capitalize compound names.

    Args:
        object (object): Usually an NPC, to have it's name capitalized before printing
        to the player.
        looker (object): The entity looking at the object to get it's capitalized name,
        usually already set before passing.
    
    Return:
        str: the name with it's first letter capitalized.
    """
    return (obj.get_display_name(looker)[0].upper() + obj.get_display_name(looker)[1:])

def is_sitting_msg(character):
    """
    This exists only to have a single place to edit the 'not standing move error' text.

    Args:
        character (object): The character trying to move between rooms.
    """

    if character.db.stance == 'sitting':
        return character.msg("Shouldn't you stand upright first?")
