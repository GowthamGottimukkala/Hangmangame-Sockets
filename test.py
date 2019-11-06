from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.uix.label import Label
from kivy.uix.anchorlayout import AnchorLayout

FPS = 1 / 60  # frames per second
WINDOWWIDTH = 500  # size of window's with in pixels
WINDOWHEIGHT = 600  # size of window's height in pixels
NUM_OF_GUESSES = 4  # number of guesses before game over
INNER_MARGIN = 15  # distance of inner border from window edge in pixels
OUTER_MARGIN = 10  # distance of outer border from window edge in pixels
LINE_LENGTH = 13  # length of single line of a capital letter.

#           R    G    B    A
SALMON = (0.58, 0.24, 0.28, 1.00)
GOLD = (1.00, 0.84, 0.00, 1.00)
WHITE = (1.00, 1.00, 1.00, 1.00)
FADED_WHITE = (1.00, 1.00, 1.00, 0.30)
LIGHT_RED = (1.00, 0.00, 0.00, 0.50)
LIGHT_GREEN = (0.00, 1.00, 0.00, 0.50)
NO_COLOR = (0.00, 0.00, 0.00, 0.00)

class HangmanApp(App):
    # App that runs Hangman game.
    # Configuration Settings
    Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
    Config.set('graphics', 'resizable', 0)
    Config.set('graphics', 'width', WINDOWWIDTH)
    Config.set('graphics', 'height', WINDOWHEIGHT)

    # Makes constant variables avaiable to hangman.kv file
    IM = INNER_MARGIN
    OM = OUTER_MARGIN
    BACKGROUND_COLOR = SALMON
    BORDER_LINE_COLOR = GOLD
    BODY_COLOR = NO_COLOR
    GALLOW_COLLOR = GOLD
    def build(self):
        return Label(text='Hello world')
if __name__ == '__main__':
    HangmanApp().run()