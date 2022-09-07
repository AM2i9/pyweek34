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

        self.level = Level("assets/levels/pysa_headquarters_rocket.tmx")

        self.lem_path = self.level.get_path_to_endpoint(Lemming(self))

    def on_draw(self):

        self.clear()

        self.level.draw()

        self.lemmings.draw(pixelated=True)

        self.level.draw_foreground()

        # if self.lem_path:
        #     arcade.draw_line_strip(self.lem_path, arcade.color.RED, 2)

    def on_mouse_press(self, x, y, button, key_modifiers):
        if button == 1:
            cart_coords = self.level.map.get_cartesian(x, y)

            new_barrier = arcade.Sprite("assets/tiles/barrier.png")

            new_barrier.set_position(
                (cart_coords[0] * 32) + (new_barrier.width // 2),
                (cart_coords[1] * 32) + (new_barrier.height // 2),
            )

            self.level.walls.append(new_barrier)

            intercepted_point = -1

            # Check if newly placed wall intercepts the path
            for i, p in enumerate(self.lem_path):
                if arcade.is_point_in_polygon(*p, new_barrier.get_adjusted_hit_box()):
                    intercepted_point = i
                    break

            if intercepted_point != -1:

                furthest_lemming = None
                furthest_index = -1

                non_intercepted_lems = []

                for lemming in self.lemmings:

                    cur_point_index = lemming.path.index(lemming.current_path_point)

                    # Find furthest lemming not intercepted by a wall
                    if not cur_point_index >= intercepted_point:
                        if cur_point_index >= furthest_index:
                            furthest_index = cur_point_index
                            furthest_lemming = lemming

                        non_intercepted_lems.append(lemming)

                if furthest_lemming:
                    new_path = self.level.get_path_to_endpoint_from_point(
                        furthest_lemming.position, furthest_lemming
                    )

                    self.lem_path = self.lem_path[: furthest_index - 1] + new_path

                    for lem in non_intercepted_lems:
                        lem.set_path(self.lem_path)

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
