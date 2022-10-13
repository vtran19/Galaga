import arcade

SCREEN_WIDTH = 450
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Galaga"


class User(arcade.Sprite):

    def __init__(self):
        # Initializing user variables
        self.center_x = 225
        self.center_y = 50
        self.change_x = 0
        self.change_y = 0

    def update(self):
        # Updates the location of the user
        self.center_x += self.change_x
        self.center_y += self.change_y

    """
    def draw(self):
        # User dimensions and draws square, update to look better
        user_width = 15
        user_height = 15
        user_color = arcade.color.ORANGE_RED
        # Draws rec
        arcade.draw_rectangle_filled(self.center_x+self.change_x, self.center_y+self.change_y, user_width,
                                     user_height, user_color)
    """


class Game(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        # self.user_list = None

        self.user = User()

        # Set background color
        self.background_color = arcade.color.BLACK

    def setup(self):
        # sprite lists here
        self.sprite_list = []

        # User Setup
        self.user.center_x = 225
        self.user.center_y = 50
        self.user.user_width = 15
        self.user.user_height = 15
        self.user.user_color = arcade.color.ORANGE_RED
        arcade.draw_rectangle_filled(self.center_x + self.change_x, self.center_y + self.change_y,
                                     self.user.user_width, self.user.user_height, self.user.user_color)
        self.sprite_list.append(self.user)

    def on_draw(self):
        self.clear()

        # Draw all sprites in list
        self.sprite_list.draw()
        # self.user.draw()

    def on_update(self, delta_time):
        self.user.update()

    def on_key_press(self, key, modifiers):
        # If the player presses a key, update the speed
        movement_speed = 5
        if key == arcade.key.LEFT:
            self.user.change_x = -movement_speed
        elif key == arcade.key.RIGHT:
            self.user.change_x = movement_speed

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.user.change_x = 0


def main():

    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


main()

