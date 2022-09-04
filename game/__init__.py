import arcade

from game.game import Game

GAME_WIDTH = 1280
GAME_HEIGHT = 720
WINDOW_TITLE = "PyWeek3"


def main():

    game = Game(GAME_WIDTH, GAME_HEIGHT, WINDOW_TITLE)

    game.setup()
    arcade.run()
