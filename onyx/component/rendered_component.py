import onyx, pygame


class RenderedComponent(onyx.Component):
    """
    A component that gets rendered by the `App`. Must be extended
    and told how to render.

    Inheritors of `RenderedComponent` may implement the `update(delta: float)`,
    `handle(event: pygame.event.Event)`, and `render(surface: pygame.Surface)`
    methods.
    """

    def __init__(
        self,
        event_types: list[int],
        rect: pygame.Rect,
        visible: bool = True,
        z_index: int = 0,
    ) -> None:
        super().__init__(event_types)
        self.visible = visible
        self.z_index = z_index

        self._rect = rect
        self._redraw_requested = True

    @property
    def rect(self) -> pygame.Rect:
        """
        The bounding `Rect` for this component.
        """
        return self._rect

    @rect.setter
    def rect(self, value: pygame.Rect):
        self._rect = value

    def request_redraw(self):
        """
        Tells the `App` that this component needs to be redrawn.

        Call this from your `update()` or `handle()` implementations,
        for example, after the component state has changed.
        """
        self._redraw_requested = True

    def render(self, surface: pygame.Surface):
        """
        Possible override for `RenderedComponent` subclasses.

        Called at most once per `App` frame, when this component has
        requested a redraw, or if it overlaps with something that has
        been redrawn. Use this method to draw your component.

        Note: Aim to have your component's `rect` cover the region
        rendered by this method.
        """
        pass

    def _internal_render(self, surface: pygame.Surface):
        self.render(surface)
        self._redraw_requested = False
