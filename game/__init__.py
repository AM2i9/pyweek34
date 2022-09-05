import arcade

from game.game import Game

GAME_WIDTH = 704
GAME_HEIGHT = 800
WINDOW_TITLE = "PyWeek3"


def main():

    game = Game(GAME_WIDTH, GAME_HEIGHT, WINDOW_TITLE)

    game.setup()
    arcade.run()
