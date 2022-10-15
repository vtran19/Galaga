import arcade
import os

SCREEN_WIDTH = 450
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Galaga"

# User constants
SPRITE_SCALE_USER = 0.05
USER_SPEED = 3.0


class User(arcade.Sprite):
    """ User Class """
    def __init__(self, image, scale):
        super().__init__(image, scale)
        self.change_x = 0
        self.change_y = 0

    def update(self):
        # Updates the location of the user
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Keeps player in-bounds
        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1


class Game(arcade.Window):
    def __init__(self, width, height, title):
        # Call the parent class initializer
        super().__init__(width, height, title)

        self.user_list = None

        # Set up user info (?)
        self.user_sprite = None

        # Set background color
        self.background_color = arcade.color.BLACK

    def setup(self):
        # Sprite lists
        self.user_list = arcade.SpriteList()

        # Create user
        self.user = User(os.path.expanduser("~/Desktop/user_ship.png"), SPRITE_SCALE_USER)
        # set user initial position
        self.user.center_x = 225
        self.user.center_y = 50

        # append user to user_list
        self.user_list.append(self.user)

    def on_update(self, delta_time):
        self.user_list.update()

    def on_draw(self):
        arcade.start_render()
        self.clear()

        # Draws sprites
        self.user_list.draw()

    def on_key_press(self, key, modifiers):
        # If the player presses a key, update the speed
        if key == arcade.key.LEFT:
            self.user.change_x = -USER_SPEED
        elif key == arcade.key.RIGHT:
            self.user.change_x = USER_SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.user.change_x = 0


def main():

    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


main()

