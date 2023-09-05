import onyx, pygame


class Square(onyx.RenderedComponent):
    MOVE_SPEED = 80

    def __init__(self, pos: pygame.Vector2, size: int = 20) -> None:
        rect = pygame.Rect(0, 0, size, size)
        rect.center = (pos.x, pos.y)

        super().__init__([], rect)

        self.pos = pos

    def get_input(self) -> pygame.Vector2:
        right, left, down, up = self.app.get_key_states(
            pygame.K_RIGHT, pygame.K_LEFT, pygame.K_DOWN, pygame.K_UP
        )
        return pygame.Vector2(right - left, down - up)

    # Below are Onyx Component/RenderedComponent methods
    def update(self, delta: float):
        key_input = self.get_input()
        if key_input.magnitude_squared() != 0:
            # self.pos tracks a non-truncated position
            self.pos += key_input.normalize() * Square.MOVE_SPEED * delta

            # Perform collisions with app bounds using self.rect.
            if not self.app.rect.contains(self.rect):
                self.rect.clamp_ip(self.app.rect)
                self.pos = pygame.Vector2(*self.rect.center)

            self.rect.center = (self.pos.x, self.pos.y)

            # Tell Onyx that something has changed.
            self.request_redraw()

    def render(self, surface: pygame.Surface):
        surface.fill("white", self.rect)


if __name__ == "__main__":
    scene = onyx.Scene("square", [Square(pygame.Vector2(150, 100))])

    onyx.App(
        dimensions=[300, 200],
        scenes=[scene],
    ).run()
