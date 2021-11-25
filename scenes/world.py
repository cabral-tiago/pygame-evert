from classes.level import Level
from classes.scene import Scene
from pygame.surface import Surface


class World(Scene):
    def __init__(self) -> None:
        super().__init__()

        self.level_1: Level = Level("assets/levels/1")

    def draw(self, screen: Surface) -> None:
        self.level_1.draw(screen)
        super().draw(screen)
