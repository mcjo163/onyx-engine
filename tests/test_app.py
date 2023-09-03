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
    def test_app_initializes_pygame(self):
        _ = onyx.App()
        assert pygame.get_init()

    def test_second_app_raises_error(self):
        _ = onyx.App()
        with pytest.raises(OnyxError):
            _ = onyx.App()
