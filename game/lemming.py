from typing import Tuple
import arcade
import math

import game


class Lemming(arcade.Sprite):
    def __init__(self, game):
        super().__init__(scale=2)

        self.game = game

        self.textures = arcade.load_textures(
            "assets/images/tiny-astro-sheet-alpha.png",
            [
                (0, 0, 8, 8),  # Top row
                (8, 0, 8, 8),
                (16, 0, 8, 8),
                (0, 8, 8, 8),  # Middle row
                (8, 8, 8, 8),
                (16, 8, 8, 8),
                (0, 16, 8, 8),  # Bottom row
                (8, 16, 8, 8),
                (16, 16, 8, 8),
            ],
        )

        self.animations = {
            "front": self.textures[:3],
            "left": self.textures[3:6],
            "right": [ # Generate right-facing textures
                arcade.Texture(f"right_{i}", t.image.transpose(0))
                for i, t in enumerate(self.textures[3:6])
            ],
            "back": self.textures[6:],
        }

        self.current_animation = None
        self.current_texture = 0

        self.texture = self.textures[0]

        self.speed = 2
        self.at_position = False

        self.path = None
        self.path_iter = None
        self.current_path_point = None

        self.dest = None

    def update_animation(self, delta_time: float):

        int_x = int(self.change_x)
        int_y = int(self.change_y)

        if int_x > 0:
            self.current_animation = "right"
        elif int_x < 0:
            self.current_animation = "left"

        if int_y > 0:
            self.current_animation = "back"
        elif int_y < 0:
            self.current_animation = "front"

        self.texture = self.animations[self.current_animation][
            self.current_texture // 6
        ]
        self.current_texture += 1
        if self.current_texture > 12:
            self.current_texture = 0

    def set_destination(self, dest: Tuple[int, int]):
        self.dest = dest

    def set_path(self, path):
        self.path = path
        next_closest = self.get_path_from_next_closest_point()
        self.path_iter = iter(next_closest)
        self.current_path_point = next(self.path_iter)

    def get_path_from_next_closest_point(self):
        cur_min = 1000000000000
        min_index = 0
        for i, point in enumerate(self.path):
            distance = math.sqrt(
                (self.center_x - point[0]) ** 2 + (self.center_y - point[1]) ** 2
            )
            if distance < cur_min:
                cur_min = distance
                min_index = i

        return self.path[min_index:]

    def update(self):
        if self.current_path_point:
            angle = math.atan2(
                self.current_path_point[1] - self.center_y,
                self.current_path_point[0] - self.center_x,
            )

            distance = math.sqrt(
                (self.center_x - self.current_path_point[0]) ** 2
                + (self.center_y - self.current_path_point[1]) ** 2
            )

            speed = min(self.speed, distance)

            self.change_x = math.cos(angle) * speed
            self.change_y = math.sin(angle) * speed

            self.center_x += self.change_x
            self.center_y += self.change_y

            distance = math.sqrt(
                (self.center_x - self.current_path_point[0]) ** 2
                + (self.center_y - self.current_path_point[1]) ** 2
            )

            if distance <= self.speed:
                self.current_path_point = next(self.path_iter, None)
                if self.current_path_point is None:
                    self.path = None
                    self.path_iter = None
                    self.remove_from_sprite_lists()
