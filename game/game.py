import random
import time

import arcade

import game
from game.lemming import Lemming


class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        self.lemmings = None

    def setup(self):
        
        self.lemmings = arcade.SpriteList()

        for i in range(500):
            new_lem = Lemming()

            new_lem.set_position(32, 840-32)
            
            self.lemmings.append(new_lem)

    def on_draw(self):

        self.clear()

        self.lemmings.draw(pixelated=True)
    
    def on_update(self, delta_time: float):
        self.lemmings.update()
        self.lemmings.update_animation(delta_time)
