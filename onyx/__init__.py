"""
Onyx is a lightweight abstraction built on top of the excellent
pygame library.

The main object provided by Onyx is the `App` class that encapsulates
many common pygame patterns such as a game loop, event handling, and
maintaining and rendering game objects.

Please note, your program should only make use of one Onyx `App` class,
since pygame is only designed to handle one window.
"""
import os

# Hide pygame's import output
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

from onyx.app import App
from onyx.scene import Scene
from onyx.component.component import Component
from onyx.component.rendered_component import RenderedComponent

# Clean up namespace.
del os
