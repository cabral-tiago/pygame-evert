from classes.enums import GameState, SceneID
from classes.scene import Scene
from scenes.deathscreen import DeathScreen
from scenes.menu import Menu
from scenes.world import World


class Game:
    def __init__(self) -> None:
        self.__state = GameState.MAIN_MENU

        self.__scenes: dict[SceneID, Scene] = {}
        
        self.__scenes[SceneID.MENU] = Menu()
        self.__scenes[SceneID.WORLD] = World()
        self.__scenes[SceneID.DEATHSCREEN] = DeathScreen()
        self.__current_scene = SceneID.MENU

    def update(self, dt) -> None:
        # Update current scene
        result = self.__scenes[self.__current_scene].update(dt)
        self.change_state(result)

    def draw(self, screen) -> None:
        self.__scenes[self.__current_scene].draw(screen)

    def change_state(self, new_state: GameState) -> None:
        self.__state = new_state

        match self.__state:
            case GameState.MAIN_MENU:
                self.__current_scene = SceneID.MENU
            case GameState.GAME_FRESH:
                self.__scenes[SceneID.WORLD].reset()
                self.__current_scene = SceneID.WORLD
            case GameState.GAME_DEAD:
                self.__current_scene = SceneID.DEATHSCREEN
            case GameState.GAME_RETRY_LEVEL:
                self.__scenes[SceneID.WORLD].reset_level()
                self.__current_scene = SceneID.WORLD
            case GameState.GAME_NEXT_DIALOGUE:
                self.get_current_scene().get_next_dialogue()
            case GameState.GAME_LEVEL_END:
                self.change_state(self.get_current_scene().goto_next_level())
            case GameState.GAME_END:
                self.__current_scene = SceneID.MENU
    
    def get_current_scene(self) -> Scene:
        return self.__scenes[self.__current_scene]

    def handle_mouse_click(self) -> None:
        new_state = self.__scenes[self.__current_scene].handle_mouse_click()

        if new_state != GameState.NULL:
            self.change_state(new_state)

    def handle_key_down(self, key: int) -> None:
        new_state = self.__scenes[self.__current_scene].handle_key_down(key)
        self.change_state(new_state)
    
    def handle_key_up(self, key: int) -> None:
        new_state = self.__scenes[self.__current_scene].handle_key_up(key)
        self.change_state(new_state)
