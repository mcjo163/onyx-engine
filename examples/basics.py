import onyx, pygame


class Square(onyx.RenderedComponent):
    MOVE_SPEED = 80

    def __init__(self, pos: pygame.Vector2, size: int = 20) -> None:
        rect = pygame.Rect(0, 0, size, size)
        rect.center = (pos.x, pos.y)

        super().__init__(
            [
                pygame.KEYDOWN,
                pygame.KEYUP,
            ],
            rect,
        )

        self.pos = pos
        self.velocity = pygame.Vector2(0, 0)

    def handle(self, event: pygame.event.Event):
        match event.type:
            case pygame.KEYDOWN:
                match event.key:
                    case pygame.K_RIGHT:
                        self.velocity.x = 1
                    case pygame.K_LEFT:
                        self.velocity.x = -1
                    case pygame.K_DOWN:
                        self.velocity.y = 1
                    case pygame.K_UP:
                        self.velocity.y = -1
            case pygame.KEYUP:
                match event.key:
                    case pygame.K_RIGHT | pygame.K_LEFT:
                        self.velocity.x = 0
                    case pygame.K_DOWN | pygame.K_UP:
                        self.velocity.y = 0

    def update(self, delta: float):
        if self.velocity.magnitude_squared() != 0:
            self.pos += self.velocity.normalize() * Square.MOVE_SPEED * delta

            dim = self.app.dimensions
            if not self.app.rect.contains(self.rect):
                self.rect.clamp_ip(self.app.rect)
                self.pos = pygame.Vector2(*self.rect.center)

            self.rect.center = (self.pos.x, self.pos.y)
            self.request_redraw()

    def render(self, surface: pygame.Surface):
        surface.fill("white", self.rect)


if __name__ == "__main__":
    scene = onyx.Scene("square", [Square(pygame.Vector2(150, 100))])

    onyx.App(
        dimensions=[300, 200],
        scenes=[scene],
    ).run()
