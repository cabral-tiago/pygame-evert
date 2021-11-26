from pygame.surface import Surface
from classes.button import Button
from classes.gameobject import GameObject
from classes.level import Level


class Scene:
    def __init__(self) -> None:
        self.objects: list[GameObject] = []
        self.buttons: list[Button] = []
        
        self.__levels: dict[int, Level] = {}
        self.__levels[0] = Level("assets/levels/0")
        self.__current_level = 0

    def load_level(self, level_nr: int, level: Level) -> None:
        self.__levels[level_nr] = level

    def change_level(self, level_nr: int) -> None:
        if level_nr in self.__levels.keys():
            self.__current_level = level_nr

    def get_current_level(self) -> Level:
        return self.__levels[self.__current_level]

    def update(self, dt: float) -> None:
        pass

    def draw(self, screen: Surface) -> None:
        for object in self.objects:
            screen.blit(object.get_surface(), object.get_position())
        for button in self.buttons:
            screen.blit(button.get_surface(), button.get_position())
