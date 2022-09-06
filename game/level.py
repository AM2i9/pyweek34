from typing import List
import arcade

import game
from game.lemming import Lemming


class Level:
    def __init__(self, map_file):

        self.map_file = map_file

        self.map = arcade.load_tilemap(map_file)

        self.start_point = (0, 0)
        self.end_point = (0, 0)

        for obj in self.map.object_lists.get("points", []):
            if obj.name == "start":
                self.start_point = obj.shape[0], obj.shape[1]
            elif obj.name == "end":
                self.end_point = obj.shape[0], obj.shape[1]

        kill_triggers = self.map.object_lists.get("kill_triggers", [])
        self.kill_triggers = []

        if kill_triggers:
            for trigger in kill_triggers:
                self.kill_triggers.append(
                    [(x, game.GAME_HEIGHT + y) for x, y in trigger.shape]
                )

        self.walls = self.map.sprite_lists.get("walls", arcade.SpriteList())
        self.floor = self.map.sprite_lists.get("floor", arcade.SpriteList())
        self.decoration = self.map.sprite_lists.get("deco", arcade.SpriteList())

    def draw(self):
        self.floor.draw()
        self.walls.draw()
        self.decoration.draw()

    def update(self, delta_time: float, lemmings: List[Lemming]):
        self.decoration.update_animation(delta_time)

        for lemming in lemmings:
            for trigger in self.kill_triggers:
                if arcade.is_point_in_polygon(
                    lemming.center_x, lemming.center_y, trigger
                ):
                    lemming.kill()

    def get_path_to_endpoint(self, lem):
        return self.get_path_to_endpoint_from_point(self.start_point, lem)

    def get_path_to_endpoint_from_point(self, point, lem):
        return arcade.astar_calculate_path(
            point,
            self.end_point,
            arcade.AStarBarrierList(
                lem, self.walls, 16, 0, game.GAME_WIDTH, 0, game.GAME_HEIGHT
            ),
            diagonal_movement=False,
        )
