import pygame, onyx
import pytest

from onyx.error import OnyxError


@pytest.fixture(autouse=True)
def pygame_reset():
    """
    Fixture that quits pygame if it has been initialized so that
    each App test has a clean slate.
    """
    if pygame.get_init():
        pygame.quit()


class TestApp:
    dimensions = [100, 100]

    def test_app_initializes_pygame(self):
        _ = onyx.App(dimensions=self.dimensions)
        assert pygame.get_init()

    def test_second_app_raises_error(self):
        _ = onyx.App(dimensions=self.dimensions)
        with pytest.raises(OnyxError):
            _ = onyx.App(dimensions=self.dimensions)

    def test_add_scene(self):
        app = onyx.App(dimensions=self.dimensions)
        scene = onyx.Scene("test", [onyx.Component([])])
        app.add_scene(scene)
        assert len(app._scenes) == 1
        assert scene.app == app
