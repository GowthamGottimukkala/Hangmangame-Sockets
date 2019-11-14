#!/usr/bin/env python3
import os
from random import randint
import socket
import sys

from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.uix.anchorlayout import AnchorLayout

FPS = 1 / 60  # frames per second
WINDOWWIDTH = 800  # size of window's with in pixels
WINDOWHEIGHT = 900  # size of window's height in pixels
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

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = int(sys.argv[1])
s.connect(("127.0.0.1", port))


def start_conditions():
    # Sets the starting conditions for a new game.
    print("Waiting")
    length = s.recv(1024).decode("utf-8")
    print(length)
    try:
        spaces = length.split(";")[1].split(",")
        spaces = list(map(int,spaces))
        print(spaces)
    except:
        pass
    length = length.split(";")[0]
    print(length)
    category = s.recv(1024).decode("utf-8")
    hidden_word = []
    for i in range(int(length)):
        if(i in spaces):
            hidden_word.append(" ")
        else:
            hidden_word.append("_")
    print(hidden_word)
    # hidden_word = ['_' for i in range(int(length))]
    misses = 0

    return category, hidden_word, misses


class HangmanBoard(AnchorLayout):
    category, hidden_word, misses = start_conditions()
    def calling(self,letter):
        self.letter_click(letter)
        self.hangman_body()
        self.win_or_lose()
        # self.add_money()

    def add_money(self,competition):
        self.ids["guesses"].text = str(competition)

    def update(self, dt):
        # renders updates of guesses and hidden word, and checks if the game is
        # won or not

        self.ids['category'].text = self.category
        self.ids['hidden'].text = ' '.join(self.hidden_word)


    def win_or_lose(self):
        # checks if the game is won or not
        print(self.hidden_word)
        s.send(bytes("".join(self.hidden_word),"utf-8"))
        yesno = s.recv(1024).decode("utf-8")
        print(yesno)
        if(yesno == "yes"):
            self.disable_letters()
            s.send(bytes("completed","utf-8"))
        elif NUM_OF_GUESSES == self.misses:
            self.disable_letters()
            s.send(bytes("notcompleted","utf-8"))
        else:
            s.send(bytes("continue","utf-8"))
        status = s.recv(1024).decode("utf-8")
        if("unable" in status):
            status2 = s.recv(1024).decode("utf-8")
            print(status2)
            self.add_money(status2)
        elif("guessed" in status):
            status2 = s.recv(1024).decode("utf-8")
            print(status2)
            self.add_money(status2)
        print(status)
        

    def hangman_body(self):
        # draws/reveals the hangman body

        body = self.ids['gallows'].canvas.get_group('body')
        if self.misses == 1:
            body[0].rgba = WHITE  # the head
        elif self.misses == 2:
            body[1].rgba = WHITE  # the body
        elif self.misses == 3:
            body[2].rgba = WHITE  # the arms
        elif self.misses == 4:
            body[3].rgba = WHITE  # the legs

    def letter_click(self, letter):
        # Checks if clicked letter is in the word or not

        letter.disabled = True
        letter.disabled_color = WHITE

        guess = letter.text.lower()

        # sets letter background to red
        letter.background_color = LIGHT_RED
        s.send(bytes(guess,"utf-8"))
        indexes = s.recv(1024).decode("utf-8")
        values = s.recv(1024).decode("utf-8")
        print("values-",values)
        print()
        competition = s.recv(1024).decode("utf-8")
        print(competition)
        self.add_money(competition)
        if(indexes=="no"):
            self.misses += 1
        else:
            indexes = indexes.split(",")
            print("indexes-",indexes)
            indexeslis = [int(x) for x in indexes]
            p = 0
            for i in indexeslis:
                self.hidden_word[i] = values[p]
                p += 1
                letter.background_color = LIGHT_GREEN

    

    def disable_letters(self):
        for k, v in self.ids.items():
            if k[0:6] == 'letter' and v.disabled is False:
                v.disabled = True
                v.disabled_color = GOLD

    # def enable_letters(self):
    #     # enables letter buttons

    #     for k, v in self.ids.items():
    #         if k[0:6] == 'letter':
    #             v.disabled = False
    #             v.background_color = SALMON

    # def new_game(self):
    #     # refreshes game board with new game.

    #     t = start_conditions()
    #     self.category, self.word, self.hidden_word, self.misses = t

    #     self.enable_letters()

    #     body = self.ids['gallows'].canvas.get_group('body')
    #     for parts in body:
    #         parts.rgba = NO_COLOR


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
        game = HangmanBoard()
        Clock.schedule_interval(game.update, FPS)
        return game

HangmanApp().run()


