import math
import logging
import arcade
import pymunk

from game_object import Bird, Column, Pig, YellowBird, BlueBird
from game_logic import get_impulse_vector, Point2D, get_distance

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("arcade").setLevel(logging.WARNING)
logging.getLogger("pymunk").setLevel(logging.WARNING)
logging.getLogger("PIL").setLevel(logging.WARNING)

logger = logging.getLogger("main")

WIDTH = 1320
HEIGHT = 630
TITLE = "Angry birds"
GRAVITY = -900


class App(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = arcade.load_texture("assets/img/background3.png")
        # crear espacio de pymunk
        self.space = pymunk.Space()
        self.space.gravity = (0, GRAVITY)

        # agregar piso
        floor_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        floor_shape = pymunk.Segment(floor_body, [0, 15], [WIDTH, 15], 0.0)
        floor_shape.friction = 10
        self.space.add(floor_body, floor_shape)

        self.activating_power = False
        self.changing_level = False
        self.bird_turn = 0
        self.bird_types = [Bird, YellowBird, BlueBird]

        self.score = 0
        self.current_level = 1
        self.required_score = 100
        self.next_level_unlocked = False

        self.sprites = arcade.SpriteList()
        self.birds = arcade.SpriteList()
        self.world = arcade.SpriteList()

        self.add_columns()
        self.add_pigs()

        self.start_point = Point2D()
        self.end_point = Point2D()
        self.distance = 0
        self.draw_line = False

        # agregar un collision handler
        self.handler = self.space.add_default_collision_handler()
        self.handler.post_solve = self.collision_handler

        self.level_cleared_texture = arcade.load_texture("assets/img/level-cleared.png")
        self.next_level_texture = arcade.load_texture("assets/img/next-level.png")
        self.sling_texture = arcade.load_texture("assets/img/sling-3.png")

    def collision_handler(self, arbiter, space, data):
        impulse_norm = arbiter.total_impulse.length
        if impulse_norm < 100:
            return True
        logger.debug(impulse_norm)
        if impulse_norm > 1200:
            for obj in self.world:
                if obj.shape in arbiter.shapes:
                    obj.remove_from_sprite_lists()
                    self.space.remove(obj.shape, obj.body)
                    if isinstance(obj, Pig):
                        self.score += 100
                    else:
                        self.score += 25

        return True

    def add_columns(self):
        if self.current_level == 1:
            positions = [(WIDTH // 2, 50), (WIDTH // 2 + 400, 50)]
        elif self.current_level == 2:
            positions = [(WIDTH // 2, 50), (WIDTH // 2 + 250, 50), (WIDTH // 2 + 500, 50)]
        else:
            positions = [(WIDTH // 2, 50), (WIDTH // 2 + 200, 50), (WIDTH // 2 + 400, 50), (WIDTH // 2 + 600, 50)]

        for x, y in positions:
            column = Column(x, y, self.space)
            self.sprites.append(column)
            self.world.append(column)

    def add_pigs(self):
        if self.current_level == 1:
            positions = [(WIDTH / 2, 100)]
        elif self.current_level == 2:
            positions = [(WIDTH / 2, 100), (WIDTH / 2 + 250, 100)]
        else:
            positions = [(WIDTH / 2, 100), (WIDTH / 2 + 200, 100), (WIDTH / 2 + 400, 100)]

        for x, y in positions:
            pig = Pig(x, y, self.space)
            self.sprites.append(pig)
            self.world.append(pig)

    def load_next_level(self):
        self.current_level += 1
        self.score = 0
        self.next_level_unlocked = False
        self.required_score += 100
        self.bird_turn = 0

        self.sprites.clear()
        self.birds.clear()
        self.world.clear()

        self.space = pymunk.Space()
        self.space.gravity = (0, GRAVITY)

        floor_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        floor_shape = pymunk.Segment(floor_body, [0, 15], [WIDTH, 15], 0.0)
        floor_shape.friction = 10
        self.space.add(floor_body, floor_shape)

        self.add_columns()
        self.add_pigs()

        self.handler = self.space.add_default_collision_handler()
        self.handler.post_solve = self.collision_handler

    def on_update(self, delta_time: float):
        self.space.step(1 / 60.0)  # actualiza la simulacion de las fisicas
        self.sprites.update(delta_time)
        if self.score >= self.required_score:
            self.next_level_unlocked = True

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.next_level_unlocked:
                next_level_button_y = HEIGHT // 2 - 115
                if WIDTH // 2 - 60 <= x <= WIDTH // 2 + 60 and next_level_button_y - 60 <= y <= next_level_button_y + 60:
                    self.changing_level = True
                    self.load_next_level()
                return

            for bird in self.birds:
                if isinstance(bird, YellowBird) and not bird.used_power:
                    bird.activate_power()
                    self.activating_power = True
                    return

                if isinstance(bird, BlueBird) and not bird.used_power:
                    new_birds = bird.activate_power(self.space)

                    for new_bird in new_birds:
                        self.sprites.append(new_bird)
                        self.birds.append(new_bird)

                    bird.remove_from_sprite_lists()
                    self.space.remove(bird.shape, bird.body)

                    self.activating_power = True
                    return
            self.start_point = Point2D(x, y)
            self.end_point = Point2D(x, y)
            self.draw_line = True
            logger.debug(f"Start Point: {self.start_point}")


    def on_mouse_drag(self, x: int, y: int, dx: int, dy: int, buttons: int, modifiers: int):
        if buttons == arcade.MOUSE_BUTTON_LEFT:
            self.end_point = Point2D(x, y)
            logger.debug(f"Dragging to: {self.end_point}")

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        if self.changing_level:
            self.changing_level = False
            return
        if self.next_level_unlocked:
            return
        if self.activating_power:
            self.activating_power = False
            return
        if button == arcade.MOUSE_BUTTON_LEFT:
            logger.debug(f"Releasing from: {self.end_point}")
            self.draw_line = False
            impulse_vector = get_impulse_vector(self.start_point, self.end_point)
            bird_type = self.bird_types[self.bird_turn % len(self.bird_types)]
            if bird_type == Bird:
                bird = Bird("assets/img/red-bird3.png", impulse_vector, x, y, self.space)
            elif bird_type == YellowBird:
                bird = YellowBird(impulse_vector, x, y, self.space)
            else:
                bird = BlueBird(impulse_vector, x, y, self.space)
            self.bird_turn += 1
            self.sprites.append(bird)
            self.birds.append(bird)

    def on_draw(self):
        self.clear()
        # arcade.draw_lrwh_rectangle_textured(0, 0, WIDTH, HEIGHT, self.background)
        arcade.draw_texture_rect(self.background, arcade.LRBT(0, WIDTH, 0, HEIGHT))
        self.sprites.draw()
        arcade.draw_text(f"Points: {self.score}", 18, HEIGHT - 42, arcade.color.BLACK, 22, bold=True)
        arcade.draw_text(f"Points: {self.score}", 20, HEIGHT - 40, arcade.color.WHITE, 22, bold=True)

        arcade.draw_text(f"Level {self.current_level}", 18, HEIGHT - 72, arcade.color.BLACK, 22, bold=True)
        arcade.draw_text(f"Level {self.current_level}", 20, HEIGHT - 70, arcade.color.WHITE, 22, bold=True)
        if self.next_level_unlocked:
            arcade.draw_texture_rect(self.level_cleared_texture, arcade.XYWH(WIDTH // 2, HEIGHT // 2, 650, 420))
            arcade.draw_texture_rect(self.next_level_texture, arcade.XYWH(WIDTH // 2, HEIGHT // 2 - 115, 120, 120))
        if self.draw_line:
            sling_width = 180
            sling_height = 180

            # ajusta el centro para que la abertura del sling quede en start_point
            sling_x = self.start_point.x + 35
            sling_y = self.start_point.y - 25

            arcade.draw_texture_rect(
                self.sling_texture,
                arcade.XYWH(sling_x, sling_y, sling_width, sling_height)
            )

            arcade.draw_line(
                self.start_point.x,
                self.start_point.y,
                self.end_point.x,
                self.end_point.y,
                arcade.color.BLACK,
                3
            )


def main():
    window = arcade.Window(WIDTH, HEIGHT, TITLE)
    window.center_window()
    game = App()
    window.show_view(game)
    arcade.run()


if __name__ == "__main__":
    main()