import onyx, pygame

import onyx.scene

from onyx.error import OnyxInternalError


class Component:
    """
    The most basic App component, which must be extended. A `Component`
    simply holds a list of pygame events that it cares about and is
    told when those events arise.

    Inheritors of `Component` may implement the `update()` and
    `handle()` methods to define custom behavior.
    """

    def __init__(self, event_types: list[int]) -> None:
        self._event_types = event_types

        self._scene: onyx.scene.Scene = None

    @property
    def event_types(self) -> list[int]:
        """The `pygame.event.Event` types supported by this `Component`."""
        return self._event_types

    @property
    def scene(self) -> onyx.Scene:
        """The `Scene` containing this component."""
        if not self._scene:
            raise OnyxInternalError(
                f"Component._scene is None for component: '{type(self)}'. "
                "Make sure you call Scene.add_component() or pass the component "
                "on initialization"
            )
        return self._scene

    @property
    def app(self) -> onyx.App:
        """The `App` containing this component."""
        return self.scene.app

    def handle(self, event: pygame.event.Event):
        """
        Possible override for `Component` subclasses.

        Called when pygame events that this component cares about are raised.
        Use this method to handle these events.
        """
        pass

    def _handle_raw(self, event: pygame.event.Event):
        if event.type not in self.event_types:
            raise OnyxInternalError(
                f"{type(self)} was dispatched an event it cannot handle: "
                f"{pygame.event.event_name(event.type)}"
            )
        self.handle(event)

    def update(self, delta: float):
        """
        Possible override for `Component` subclasses.

        Called once per `App` frame. Use this method to update any internal
        state for your component.
        """
        pass
