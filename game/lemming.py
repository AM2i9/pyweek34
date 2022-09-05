from typing import Tuple
import arcade
import math

import game


class Lemming(arcade.Sprite):
    def __init__(self, game):
        super().__init__(scale=3)

        self.game = game

        self.textures = arcade.load_textures(
            "assets/images/tiny-astro-sheet-alpha.png", [(0, 0, 8, 8)]
        )
        self.texture = self.textures[0]

        self.speed = 2
        self.at_position = False

        self.path = None
        self.path_iter = None
        self._current_path_point = None

        self.dest = None

    def update_animation(self, delta_time: float):
        self.texture = self.textures[0]

    def set_destination(self, dest: Tuple[int, int]):
        self.dest = dest

    def update(self):
        pass

    # if self.dest:
    #     self.path = arcade.astar_calculate_path(
    #         self.position,
    #         self.dest,
    #         arcade.AStarBarrierList(self, self.game.level.walls, 32, 0, game.GAME_WIDTH, 0, game.GAME_HEIGHT),
    #         diagonal_movement=False,
    #     )
    #     if self.path is not None:
    #         self._current_path_point = self.path[0]
    #     else:
    #         return

    # angle = math.atan2(
    #     self._current_path_point[1] - self.center_y,
    #     self._current_path_point[0] - self.center_x,
    # )

    # distance = math.sqrt(
    #     (self.center_x - self._current_path_point[0]) ** 2
    #     + (self.center_y - self._current_path_point[1]) ** 2
    # )

    # speed = min(self.speed, distance)

    # self.center_x += math.cos(angle) * speed
    # self.center_y += math.sin(angle) * speed

    # distance = math.sqrt(
    #     (self.center_x - self._current_path_point[0]) ** 2
    #     + (self.center_y - self._current_path_point[1]) ** 2
    # )

    # if distance <= self.speed:
    #     self._current_path_point = next(self.path_iter, None)
    #     if self._current_path_point is None:
    #         self.path = None
