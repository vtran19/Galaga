import arcade
import os

SCREEN_WIDTH = 450
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Galaga"

#Enemy Constants
SPRITE_SCALING_ENEMY = 0.5
ENEMY_SPEED = 3.0
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

        #Destination
        dest_x = self.position_list[self.cur_position][0]

        #find distance
        distance = dest_x - start_x

        #calculate speed, use minimum function to make sure we don't overshoot dest
        speed = min(self.speed, distance)

        #calculate change x 
        if(distance > 0):
            change_x = speed
        else:
            change_x = -speed
        #update enemy center_x to reflect movement
        self.center_x += change_x

        #update self.cur_position so enemy moves back and forth between two positions
        if self.cur_position == self.position_list[0][0]:
            self.cur_position += 1
        else:
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
        position_list = [[200,200],[300,200]]

        #Create enemy
        enemy = Enemy("./resources/images/enemy/bug.png", SPRITE_SCALING_ENEMY, position_list)
        #Set enemy initial position
        enemy.center_x = position_list[0][0]
        enemy.center_y = position_list[0][1]

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

