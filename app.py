from operator import truediv
from tokenize import Pointfloat
import arcade
import os
import math

SCREEN_WIDTH = 450
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Galaga"

#Enemy Constants
SPRITE_SCALING_ENEMY = 2
ENEMY_SPEED = .75
NUM_ENEMY_1 = 20
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

    def draw(self):
        # User dimensions and draws square, update to look better
        user_width = 15
        user_height = 15
        user_color = arcade.color.ORANGE_RED
        # Draws rec
        arcade.draw_rectangle_filled(self.center_x+self.change_x, self.center_y+self.change_y, user_width,
                                     user_height, user_color)

    def avoid_boundaries(self):
        # Makes sure user never goes beyond the edges of the screen
        if self.left <= 0:
            self.center_x += 5 
            self.left += 5
            self.right += 5
        if self.right >= SCREEN_WIDTH:
            self.center_x -= 5
            self.right -= 5
            self.left -= 5
        if self.top >= SCREEN_HEIGHT:
            self.center_y -= 5
            self.top -= 5
            self.bottom -= 5
        if self.bottom <=0:
            self.center_y += 5
            self.top += 5
            self.bottom += 5


    

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

        #List of initial points the first enemy will travel too 
        position_list = [[250,200],
                        [225,200],
                        [250,200],
                        [275,200]]

        #Generate list of enemies in two different rows
        for i in range(NUM_ENEMY_1/2):
            for point in position_list:
                newPoint = [point[0]+50,point[1]]
                position_list.insert(i, newPoint)
            enemy = Enemy("./resources/images/enemy/bug.png", SPRITE_SCALING_ENEMY, position_list)
            self.enemy_list.append(enemy)
        #Set enemy initial position
        enemy.center_x = 250
        enemy.center_y = 200
        
        #append enemy to enemy_list
        self.enemy_list.append(enemy)
                


    def on_update(self, delta_time):
        self.user.update()
        self.enemy_list.update()

        self.user.avoid_boundaries()
        
        # TODO: If user collides with rocket (rocket isn't made yet)
        # store in list
        # colliding_with = arcade.check_for_collision_with_list(
        #     self.user, #TODO: put list of potential colliding items here (missles)
        # )

        #TODO: Loop through  olliding_with and take away a life etc.


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

