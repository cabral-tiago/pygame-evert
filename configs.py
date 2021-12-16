# Debug
DEBUG = False

# Screen
SCREEN_W = 1280
SCREEN_H = 720
SCREEN_SIZE = (SCREEN_W, SCREEN_H)
BAR_HEIGHT = 54
WINDOW_TITLE = "Olá Evert"
MAX_FPS = 144

# Character sizes
__CHAR_SIZE_PER_SCREEN = {
    (1280, 720) : (500, 600),
    (1920, 1080) : (700, 840),
    (2560, 1440) : (1000, 1200)
}
CHARACTER_SIZE = __CHAR_SIZE_PER_SCREEN[SCREEN_SIZE]
