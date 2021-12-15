from enum import Enum


class GameState(Enum):
    NULL = -1
    MAIN_MENU = 0
    GAME_FRESH = 1
    GAME_DEAD = 2
    GAME_PAUSE = 3
    GAME_NEXT_DIALOGUE = 4
    GAME_OK = 5
    GAME_LEVEL_END = 6
    GAME_END = 7
    GAME_RETRY_LEVEL = 8
    GAME_UNPAUSE = 9
    EXIT = 10


class SceneID(Enum):
    MENU = 0
    WORLD = 1
    DEATHSCREEN = 2
    PAUSESCREEN = 3


class LevelType(Enum):
    BLANK = 0
    DIALOGUE = 1
    MAP = 2


class Direction(Enum):
    DOWN = 0
    UP = 1
    RIGHT = 2
    LEFT = 3
    STAY = 4


class QuestType(Enum):
    NULL = -1
    COLLECT = 0
    KILL_BOSS = 1
    KILL_MONSTERS = 2


class EndCondition(Enum):
    NULL = -1
    RETURN_WHEN_DONE = 0
    IMMEDIATE_END = 1
