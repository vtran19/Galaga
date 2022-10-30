from operator import truediv
from tokenize import Pointfloat
import arcade
import os
import math
import random
from time import perf_counter


SCREEN_WIDTH = 450
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Galaga"

# Background Constants
BACKGROUND_SPRITE_SPEED = 100
BACKGROUND_SPRITE_FREQ = 75
BACKGROUND_SPRITE_SIZE = 2

# user Constants
SPRITE_SCALE_USER = 0.04
USER_SPEED = 2.0

# Enemy Constants
SPRITE_SCALING_ENEMY = 2
ENEMY_SPEED = 2
NUM_ENEMY_1 = 20


class Enemy(arcade.Sprite):
    """
        Class to represent enemies on the screen. Likely to split up into more than one class
        later to reflect different enemy types
    """
    def __init__(self, image, scale, position_list):
        # timer for enemy lifespan related to movement, start timer
        self.start_time = perf_counter()
        # when should the enemy randomly dive 
        self.dive_time = random.uniform(self.start_time + 10, self.start_time + 60)
        # dive x location, needs to remain constant 
        self.dive_dest = [random.randint(0, 450), -20]

        super().__init__(image, scale)
        self.position_list = position_list
        self.cur_position = 0
        self.speed = ENEMY_SPEED

    def update(self):
        """Make enemies follow a path. To start, enemies move side to side"""
        # Start location
        start_x = self.center_x
        start_y = self.center_y

        # Calculate enemy lifespan to see if the enemy should dive towards the player
        if self.dive_time <= (perf_counter() - self.start_time):
            dest_x = self.dive_dest[0]
            dest_y = self.dive_dest[1]
            self.speed = 5
        else:
            # Destination
            dest_x = self.position_list[self.cur_position][0]
            dest_y = self.position_list[self.cur_position][1]

        # Find x and y diff between two locations
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y

        # update position list when enemy is at the edge so it moves down
        if self.center_x in [25, 425]:
            for i in range(0, 4):
                self.position_list[i][1] = self.position_list[i][1] - 50

        # Calculate angle to get there
        angle = math.atan2(y_diff, x_diff)

        # How far are we?
        distance = math.sqrt((self.center_x - dest_x) ** 2 + (self.center_y - dest_y) ** 2)

        # calculate speed, use minimum function to make sure we don't overshoot dest
        speed = min(self.speed, distance)

        # update enemy center_x to reflect movement
        self.center_x += math.cos(angle) * speed
        self.center_y += math.sin(angle) * speed

        # find distance
        distance = math.sqrt((self.center_x - dest_x) ** 2 + (self.center_y - dest_y) ** 2)

        # update self.cur_position so enemy moves back and forth between two positions
        if distance == 0:
            self.cur_position += 1
            if self.cur_position >= 4:
                self.cur_position = 0
                

class User(arcade.Sprite):
    """ user Class """
    def __init__(self, image, scale):
        super().__init__(image, scale)
        self.change_x = 0
        self.change_y = 0
        self.left = 210
        self.right = 240
        self.top = 65
        self.bottom = 35

    def update(self):
        # Updates the location of the user
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.left += self.change_x
        self.right += self.change_x
        self.top += self.change_y
        self.bottom += self.change_y

        # Keeps player in-bounds
        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1


class BackgroundSprite(arcade.Sprite):
    """ Background Sprite Class"""
    def __init__(self):
        self.x = 0
        self.y = 0
        self._color = (random.randrange(256), random.randrange(256), random.randrange(256))

    def reset_pos(self):
        self.x = random.randrange(SCREEN_WIDTH)
        self.y = random.randrange(SCREEN_HEIGHT, SCREEN_HEIGHT+100)


class GameView(arcade.View):
    def __init__(self):
        # Call the parent class initializer
        super().__init__()

        # Empty Lists are made
        self.user = None
        self.enemy_list = None
        self.background_sprite_list = None

        # Set background color
        self.background_color = arcade.color.BLACK

    def setup(self):
        # Set up the user
        self.user = User("./resources/images/user/user_ship.png", SPRITE_SCALE_USER)

        # Enemy sprites
        self.enemy_list = arcade.SpriteList()
        # List of points the enemy will travel too
        position_list = [[25,500],
                        [425,500],
                        [25,500],
                        [425,500]]
        # Create enemy
        enemy = Enemy("./resources/images/enemy/bug.png", SPRITE_SCALING_ENEMY, position_list)
        # Set enemy initial position
        enemy.center_x = 225
        enemy.center_y = 500
        # append enemy to enemy_list
        self.enemy_list.append(enemy)

        # Background Sprites
        self.background_sprite_list = []
        for i in range(BACKGROUND_SPRITE_FREQ):
            background_sprite = BackgroundSprite()
            background_sprite.x = random.randrange(SCREEN_WIDTH)
            background_sprite.y = random.randrange(SCREEN_HEIGHT + 200)
            self.background_sprite_list.append(background_sprite)

    def on_update(self, delta_time):
        self.user.update()
        self.enemy_list.update()
        for background_sprite in self.background_sprite_list:
            background_sprite.y -= BACKGROUND_SPRITE_SPEED * delta_time
            if background_sprite.y < 0:
                background_sprite.reset_pos()

        # TODO: If user collides with rocket (rocket isn't made yet)
        # store in list
        # colliding_with = arcade.check_for_collision_with_list(
        #     self.user, #TODO: put list of potential colliding items here (missles)
        # )

        # TODO: Loop through  colliding_with and take away a life etc.

    def on_draw(self):
        arcade.start_render()
        self.clear()
        for background_sprite in self.background_sprite_list:
            arcade.draw_point(background_sprite.x, background_sprite.y, background_sprite.color, BACKGROUND_SPRITE_SIZE)
        self.enemy_list.draw()
        self.user.draw()

    def update_play_speed(self):
        # Calculate speed based on the keys pressed
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y = USER_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -USER_SPEED
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -USER_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = USER_SPEED

    def on_key_press(self, key, modifiers):
        # If the player presses a key, update the speed
        if key == arcade.key.LEFT:
            self.user.change_x = -USER_SPEED
        elif key == arcade.key.RIGHT:
            self.user.change_x = USER_SPEED
        elif key == arcade.key.Q:
            arcade.close_window()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.user.change_x = 0


class StartView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_sprite_list = None

    def on_show_view(self):
        arcade.set_background_color(arcade.csscolor.BLACK)
        # to reset the viewport
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def setup(self):
        # Background Sprites
        self.background_sprite_list = []
        for i in range(BACKGROUND_SPRITE_FREQ):
            background_sprite = BackgroundSprite()
            background_sprite.x = random.randrange(SCREEN_WIDTH)
            background_sprite.y = random.randrange(SCREEN_HEIGHT + 200)
            self.background_sprite_list.append(background_sprite)

    def on_update(self, delta_time):
        for background_sprite in self.background_sprite_list:
            background_sprite.y -= BACKGROUND_SPRITE_SPEED * delta_time
            if background_sprite.y < 0:
                background_sprite.reset_pos()

    def on_draw(self):
        self.clear()
        # Background Sprites
        for background_sprite in self.background_sprite_list:
            arcade.draw_point(background_sprite.x, background_sprite.y, background_sprite.color, BACKGROUND_SPRITE_SIZE)
        # Text
        arcade.draw_text("GALAGA", 110, 400, arcade.color.BLUE_GREEN, 40, font_name="Kenney Blocks")
        arcade.draw_text("         Press S to Start\nPress I for instructions\n          Press Q to quit", 120, 300,
                         arcade.color.WHITE, 20, font_name="Kenney Pixel", multiline=True, width=300)

    def on_key_press(self, key, modifiers):
        # Starts game
        if key == arcade.key.S:
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)
        # Instructions
        elif key == arcade.key.I:
            instructions_view = InstructionsView()
            # game_view.setup()
            self.window.show_view(instructions_view)
        # Quit
        elif key == arcade.key.Q:
            arcade.close_window()


class InstructionsView(arcade.View):
    def on_show_view(self):
        arcade.set_background_color(arcade.csscolor.BLACK)
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        self.clear()
        # arcade.draw_text("text", x-location, y-location, arcade.color.TEXTCOLOR, font size, font name)
        arcade.draw_text("How to Play: ", 170, 550, arcade.color.WHITE, 20, font_name="Kenney Pixel")
        # TODO: Write the instructions and rules for the game
        # TODO: Make a default font global variable and default font size (20)

        arcade.draw_text("Press R to Return to Main Menu", 20, 50, arcade.color.WHITE, 20, font_name="Kenney Pixel")
        arcade.draw_text("Press Q to Quit", 20, 20, arcade.color.WHITE, 20, font_name="Kenney Pixel")

    def on_key_press(self, key, modifiers):
        # Starts Menu
        if key == arcade.key.R:
            start_view = StartView()
            start_view.setup()
            self.window.show_view(start_view)
        # Quit
        elif key == arcade.key.Q:
            arcade.close_window()


def main():

    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = StartView()
    start_view.setup()
    window.show_view(start_view)
    arcade.run()


main()

