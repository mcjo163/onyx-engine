from __future__ import annotations
from typing import Iterable

import onyx, pygame

import onyx.scene

from onyx.error import OnyxError


class App:
    """
    The main piece provided by Onyx. Represents an application with one
    window, and handles the input dispatch, updating, and rendering of
    a set of components.

    Since `pygame.display` only manages one window at a time, only one App
    can be managed at once. An `OnyxError` will be raised if
    you try to create another (or if you try to create one after pygame
    has been initialized).
    """

    CHANGE_SCENE = pygame.event.custom_type()

    def __init__(
        self,
        *,
        title: str = "onyx app",
        dimensions: tuple[int, int],
        target_fps: float = 60,
        scenes: list[onyx.scene.Scene] = [],
    ) -> None:
        if pygame.get_init():
            raise OnyxError(
                "Your program can only define one Onyx App at once, "
                "since pygame.display can only work with one window."
            )

        pygame.init()

        pygame.display.set_caption(title)
        self._dimensions = pygame.Vector2(dimensions)
        self._window = pygame.display.set_mode(self._dimensions)
        self._clock = pygame.time.Clock()
        self._fps = target_fps
        self._redraw = True

        # Initialize App scenes.
        self._scene_index = 0
        self._scenes = scenes
        for scene in self._scenes:
            scene._app = self

    @property
    def dimensions(self) -> pygame.Vector2:
        """The dimensions of the `App` window."""
        return self._dimensions

    @property
    def rect(self) -> pygame.Rect:
        """A `pygame.Rect` representing the window."""
        return pygame.Rect(0, 0, self.dimensions.x, self.dimensions.y)

    def add_scene(self, scene: onyx.scene.Scene):
        """
        Add a `Scene` to the `App`.

        Scene names must be unique.
        """
        if not isinstance(scene, onyx.scene.Scene):
            raise OnyxError(f"Invalid scene: {scene}")

        if any([s.name == scene.name for s in self._scenes]):
            raise OnyxError(
                "Scene names must be unique "
                f"(Scene '{scene.name}' is already registered)"
            )
        scene._app = self
        self._scenes.append(scene)

    def add_scenes(self, scenes: Iterable[onyx.scene.Scene]):
        """
        Add multiple `Scene`s to the `App`.

        Scene names must be unique.
        """
        for s in scenes:
            self.add_scene(s)

    def _change_scene(self, specifier: str | int | onyx.scene.Scene):
        scene_index = 0
        match specifier:
            case str(name):
                # Scene name given.
                scene_index = next(
                    (i for i, v in enumerate(self._scenes) if v.name == name), -1
                )
                if scene_index == -1:
                    raise OnyxError(f"Unknown scene: '{name}'")

            case int(index):
                # Scene index given.
                if index >= len(self._scenes):
                    raise OnyxError(f"Invalid scene index: {index}")
                scene_index = index

            case scene if isinstance(scene, onyx.scene.Scene):
                # New Scene passed.
                self.add_scene(scene)
                scene_index = len(self._scenes) - 1

            case other:
                raise OnyxError(f"Invalid scene specifier: '{other}'")

        self._scene_index = scene_index
        self._redraw = True

    def change_scene(
        self, name: str = None, index: int = None, scene: onyx.scene.Scene = None
    ):
        """
        Requests that the `App` change its current `Scene`.

        The `Scene` may be specified by name or index (to request a `Scene`
        registered in the `App`), or a new `Scene` instance can be passed in.
        """
        if not any(arg != None for arg in [name, index, scene]):
            raise OnyxError("Missing scene specifier")

        self._change_scene(scene or name or index)

    def get_key_states(self, *keys: int) -> Iterable[bool]:
        """
        Get the 'pressed' states for any number of keyboard keys
        (using the pygame key constants).
        """
        state = pygame.key.get_pressed()
        return map(lambda k: state[k], keys)

    @property
    def _current_components(self) -> list[onyx.Component]:
        return self._scenes[self._scene_index].components if any(self._scenes) else []

    @property
    def _clear_color(self) -> pygame.Color:
        return (
            self._scenes[self._scene_index].clear_color
            if any(self._scenes)
            else pygame.Color("black")
        )

    def run(self):
        """
        Runs the Onyx App.

        Once the `App` has been run, it is unusable.
        """

        done = False
        while not done:
            # Process incoming events.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

                # Dispatch event to relevant components.
                for component in self._current_components:
                    if event.type in component.event_types:
                        component._handle_raw(event)

            # Update components.
            delta = self._clock.get_time() / 1000
            for component in self._current_components:
                component.update(delta)

            # Redraw scene if any component has requested redraw, or if
            # App has forced a redraw.
            to_render = [
                c
                for c in self._current_components
                if isinstance(c, onyx.RenderedComponent) and c.visible
            ]
            if any(map(lambda rc: rc._redraw_requested, to_render)) or self._redraw:
                self._window.fill(self._clear_color)

                for component in to_render:
                    component.render(self._window)

                # A RenderedComponent counts as a pygame 'RectValue' since
                # it has a 'rect' property. Neat!
                pygame.display.flip()
                self._redraw = False

            self._clock.tick(self._fps)

        pygame.quit()
