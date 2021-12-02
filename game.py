from classes.enums import GameState, SceneID
from classes.scene import Scene
from scenes.menu import Menu
from scenes.world import World


class Game:
    def __init__(self) -> None:
        self.__state = GameState.MAIN_MENU

        self.__scenes: dict[SceneID, Scene] = {}
        
        self.__scenes[SceneID.MENU] = Menu()
        self.__scenes[SceneID.WORLD] = World()
        self.__current_scene = SceneID.MENU

    def update(self, dt) -> None:
        # Update current scene
        self.__scenes[self.__current_scene].update(dt)

    def draw(self, screen) -> None:
        self.__scenes[self.__current_scene].draw(screen)

    def change_state(self, new_state: GameState) -> None:
        self.__state = new_state

        match self.__state:
            case GameState.MAIN_MENU:
                self.__current_scene = SceneID.MENU
            case GameState.GAME_FRESH:
                self.__current_scene = SceneID.WORLD
                self.__scenes[SceneID.WORLD].change_level(1)
            case GameState.GAME_PLAYING:
                self.__current_scene = SceneID.WORLD
                self.__scenes[SceneID.WORLD].change_level(1)

    def handle_mouse_click(self) -> None:
        new_state = self.__scenes[self.__current_scene].handle_mouse_click()

        if new_state != GameState.NULL:
            self.change_state(new_state)

    def handle_key_down(self, key: int) -> None:
        self.__scenes[self.__current_scene].handle_key_down(key)
    
    def handle_key_up(self, key: int) -> None:
        self.__scenes[self.__current_scene].handle_key_up(key)
