import threading

import arcade

from game.lemming import Lemming
from game.level import Level


class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.BLACK)

        self.lemmings = None
        self.map = None

    def setup(self):

        self.lemmings = arcade.SpriteList()

        self.level = Level("assets/levels/pysa_headquarters.tmx")

    def on_draw(self):

        self.clear()

        self.level.draw()

        self.lemmings.draw(pixelated=True)

    def on_update(self, delta_time: float):

        self.lemmings.update()
        self.lemmings.update_animation(delta_time)
        self.level.update(delta_time)
