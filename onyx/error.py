"""This module defines Onyx's custom exceptions."""


class OnyxError(Exception):
    """
    A general exception used by Onyx for certain situations like:
    - trying to create a second `App`, or creating an `App` after
    pygame has already been initialized
    - Trying to add an invalid `Component` to a `Scene`
    - etc.
    """

    pass


class OnyxInternalError(OnyxError):
    """
    An internal exception. If this is raised, something is wrong with
    the library code, and should be reported.
    """

    def __init__(self, message: str) -> None:
        super().__init__(f"Internal Onyx error: {message}. Please report this")
