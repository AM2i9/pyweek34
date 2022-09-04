from typing import Tuple
import arcade
import math

class Lemming(arcade.Sprite):
    
    def __init__(self):
        super().__init__(scale=3)

        self.textures = arcade.load_textures("assets/images/tiny-astro-sheet-alpha.png", [(0, 0, 8, 8)])

        self.speed = 3
        self.at_position = False

        self.path = None
        self.path_iter = None
        self._current_path_point = None

    def update_animation(self, delta_time: float):
        self.texture = self.textures[0]
    
    def set_destination(self, dest: Tuple[int, int]):
        self.path = arcade.astar_calculate_path(self.position, dest, arcade.AStarBarrierList(self, arcade.SpriteList(), 32, 0, 720, 0, 840), diagonal_movement=False)
        if self.path is not None:
            self.path_iter = iter(self.path)
            self._current_path_point = next(self.path_iter)
    
    def update(self):
        if self.path is None or self._current_path_point == None:
            return

        angle = math.atan2(self._current_path_point[1] - self.center_y, self._current_path_point[0] - self.center_x)

        distance = math.sqrt((self.center_x - self._current_path_point[0]) ** 2 + (self.center_y - self._current_path_point[1]) ** 2)

        speed = min(self.speed, distance)

        self.center_x += math.cos(angle) * speed
        self.center_y += math.sin(angle) * speed

        distance = math.sqrt((self.center_x - self._current_path_point[0]) ** 2 + (self.center_y - self._current_path_point[1]) ** 2)

        if distance <= self.speed:
            self._current_path_point = next(self.path_iter, None)
            if self._current_path_point is None:
                self.path = None
