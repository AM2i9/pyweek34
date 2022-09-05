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

        self.update_path = False
        self.lem_time = 0
        self.lem_count = 0

    def setup(self):

        self.lemmings = arcade.SpriteList()

        self.level = Level("assets/levels/pysa_headquarters.tmx")

        self.lem_path = self.level.get_path_to_endpoint(Lemming(self))

    def on_draw(self):

        self.clear()

        self.level.draw()

        self.lemmings.draw(pixelated=True)

        # if self.lem_path:
        #     arcade.draw_line_strip(self.lem_path, arcade.color.RED, 2)

    def on_update(self, delta_time: float):
        if self.lem_count < 100 and self.lem_time > 0.2:
            new_lem = Lemming(self)

            new_lem.set_position(*self.level.start_point)
            new_lem.set_path(self.lem_path)

            self.lemmings.append(new_lem)
            self.lem_time = 0
            self.lem_count += 1
        else:
            self.lem_time += delta_time

        self.lemmings.update()
        self.lemmings.update_animation(delta_time)   

        self.level.update(delta_time, self.lemmings)
