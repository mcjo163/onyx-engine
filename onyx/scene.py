from __future__ import annotations
from typing import Iterable

import onyx, pygame

import onyx.app

from onyx.error import OnyxError, OnyxInternalError


class Scene:
    """
    An Onyx `Scene` is essentially a list of `Component`s to be processed
    by the `App`.
    """

    def __init__(
        self,
        name: str,
        components: list[onyx.Component] = [],
        clear_color: pygame.Color = pygame.Color("black"),
    ) -> None:
        self.name = name
        self.clear_color = clear_color

        # Initialize Scene components.
        self._components = components
        for component in self._components:
            component._scene = self

        self._app: onyx.app.App = None

    @property
    def components(self) -> list[onyx.Component]:
        """
        The list of `Component` (or `Component` subclass) instances that
        are part of this scene.
        """
        return self._components

    @property
    def app(self) -> onyx.app.App:
        """The `App` containing this component."""
        if not self._app:
            raise OnyxInternalError(
                f"Scene._app is None for scene: '{self.name}'. Make sure you "
                "call App.add_scene() or pass the scene on initialization"
            )
        return self._app

    def add_component(self, component: onyx.Component):
        """Add a `Component` to the `Scene`."""
        if not isinstance(component, onyx.Component):
            raise OnyxError(f"Invalid Scene component: '{component}'")

        component._scene = self
        self._components.append(component)

    def add_components(self, components: Iterable[onyx.Component]):
        """Add multiple `Component`s to the `Scene`."""
        for c in components:
            self.add_component(c)
