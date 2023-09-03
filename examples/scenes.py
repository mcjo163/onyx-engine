import onyx, pygame
import onyx.scene


class SceneSwitcher(onyx.Component):
    def __init__(self, target_scene: str) -> None:
        super().__init__([pygame.MOUSEBUTTONDOWN])
        self.target_scene = target_scene

    def handle(self, _: pygame.event.Event):
        # We know this is a MOUSEBUTTONDOWN event
        print(f"Switching to '{self.target_scene}' scene")
        onyx.scene.change_scene(self.target_scene)


if __name__ == "__main__":
    onyx.App(
        title="scenes",
        dimensions=[300, 200],
        target_fps=20,
        scenes=[
            onyx.Scene("red", [SceneSwitcher("blue")], pygame.Color("red")),
            onyx.Scene("blue", [SceneSwitcher("red")], pygame.Color("blue")),
        ],
    ).run()
