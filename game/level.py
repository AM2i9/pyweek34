import arcade

import game


class Level:
    def __init__(self, map_file):

        self.map_file = map_file

        self.map = arcade.load_tilemap(map_file)

        self.start_point = (0, 0)
        self.end_point = (0, 0)

        for obj in self.map.object_lists.get("points", []):
            print(obj.name, obj.shape)
            if obj.name == "start":
                self.start_point = obj.shape[0], obj.shape[1]
            elif obj.name == "end":
                self.end_point = obj.shape[0], obj.shape[1]

        self.kill_triggers = self.map.object_lists.get("kill_triggers", [])

        self.walls = self.map.sprite_lists.get("walls", arcade.SpriteList())
        self.floor = self.map.sprite_lists.get("floor", arcade.SpriteList())
        self.decoration = self.map.sprite_lists.get("deco", arcade.SpriteList())

    def draw(self):

        self.floor.draw()
        self.walls.draw()
        self.decoration.draw()

    def update(self, delta_time: float):
        self.decoration.update_animation(delta_time)
