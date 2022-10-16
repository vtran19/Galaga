import arcade
import os
import math

SCREEN_WIDTH = 450
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Galaga"

#Enemy Constants
SPRITE_SCALING_ENEMY = 2
ENEMY_SPEED = .75
class Enemy(arcade.Sprite):
    """
        Class to represent enemies on the screen. Likely to split up into more than one class
        later to reflect different enemy types
    """
    def __init__(self, image, scale, position_list):
        super().__init__(image, scale)
        self.position_list = position_list
        self.cur_position = 0
        self.speed = ENEMY_SPEED

    def update(self):
        """Make enemies follow a path. To start, enemies move side to side"""
        #Start location
        start_x = self.center_x
        start_y = self.center_y

        #Destination
        dest_x = self.position_list[self.cur_position][0]
        dest_y = self.position_list[self.cur_position][1]

        #Find x and y diff between two locations
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y

        # Calculate angle to get there
        angle = math.atan2(y_diff, x_diff)

        # How far are we?
        distance = math.sqrt((self.center_x - dest_x) ** 2 + (self.center_y - dest_y) ** 2)

        #calculate speed, use minimum function to make sure we don't overshoot dest
        speed = min(self.speed, distance)

        #update enemy center_x to reflect movement
        self.center_x += math.cos(angle) * speed
        self.center_y += math.sin(angle) * speed

        #find distance
        distance = math.sqrt((self.center_x - dest_x) ** 2 + (self.center_y - dest_y) ** 2)

        #update self.cur_position so enemy moves back and forth between two positions
        if distance <= self.speed:
            self.cur_position += 1
            if self.cur_position >= len(self.position_list):
                self.cur_position = 0


class User:
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

    def draw(self):
        # User dimensions and draws square, update to look better
        user_width = 15
        user_height = 15
        user_color = arcade.color.ORANGE_RED
        # Draws rec
        arcade.draw_rectangle_filled(self.center_x+self.change_x, self.center_y+self.change_y, user_width,
                                     user_height, user_color)


class Game(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.user = None
        self.enemy_list = None

        # Set background color
        self.background_color = arcade.color.BLACK

    def setup(self):
        #Set up the user
        self.user = User()

        #Sprite Lists
        self.enemy_list = arcade.SpriteList()

        #List of points the enemy will travel too 
        position_list = [[250,200],
                        [225,200],
                        [250,200],
                        [275,200]]

        #Create enemy
        enemy = Enemy("./resources/images/enemy/bug.png", SPRITE_SCALING_ENEMY, position_list)
        #Set enemy initial position
        enemy.center_x = 250
        enemy.center_y = 200

        #append enemy to enemy_list
        self.enemy_list.append(enemy)
                


    def on_update(self, delta_time):
        self.user.update()
        self.enemy_list.update()

    def on_draw(self):
        self.clear()
        self.enemy_list.draw()
        self.user.draw()

    def on_key_press(self, key, modifiers):
        # If the player presses a key, update the speed
        if key == arcade.key.LEFT:
            self.user.change_x = -5
        elif key == arcade.key.RIGHT:
            self.user.change_x = 5

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.user.change_x = 0


def main():

    window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


main()

