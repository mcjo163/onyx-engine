import onyx, pygame


class RenderedComponent(onyx.Component):
    """
    A component that gets rendered by the `App`. Must be extended
    and told how to render.

    Inheritors of `RenderedComponent` must implement the `update()`,
    `handle()`, and `render()` methods.
    """

    def __init__(
        self,
        event_types: list[int],
        rect: pygame.Rect,
        visible: bool = True,
    ) -> None:
        super().__init__(event_types)
        self.visible = visible

        self._rect = rect
        self._redraw_requested = True

    @property
    def rect(self) -> pygame.Rect:
        """
        The bounding `Rect` for this component.

        Used by the `App` to determine what needs to be redrawn, and
        only this region is guaranteed to be rendered.
        """
        return self._rect

    def request_redraw(self):
        """
        Tells the `App` that this component needs to be redrawn.

        Call this from your `update()` or `handle()` implementations,
        for example, after the component state has changed.
        """
        self._redraw_requested = True

    def render(self, surface: pygame.Surface):
        """
        Required override for `RenderedComponent` subclasses.

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
