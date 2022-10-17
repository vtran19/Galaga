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
        #Start location
        start_x = self.center_x
        start_y = self.center_y

        # calulate enemy lifespan to see if the enemy should dive towards the player
        if self.dive_time <= (perf_counter() - self.start_time):
            dest_x = self.dive_dest[0]
            dest_y = self.dive_dest[1]
            self.speed = 5
        else:
            #Destination
            dest_x = self.position_list[self.cur_position][0]
            dest_y = self.position_list[self.cur_position][1]

        #Find x and y diff between two locations
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

        #calculate speed, use minimum function to make sure we don't overshoot dest
        speed = min(self.speed, distance)

        #update enemy center_x to reflect movement
        self.center_x += math.cos(angle) * speed
        self.center_y += math.sin(angle) * speed

        #find distance
        distance = math.sqrt((self.center_x - dest_x) ** 2 + (self.center_y - dest_y) ** 2)

        #update self.cur_position so enemy moves back and forth between two positions
        if distance == 0:
            self.cur_position += 1
            if self.cur_position >= 4:
                self.cur_position = 0
                
        



class User(arcade.Sprite):
    """ User Class """
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
        # Call the parent class initializer
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
        position_list = [[25,500],
                        [425,500],
                        [25,500],
                        [425,500]]

        #Create enemy
        enemy = Enemy("./resources/images/enemy/bug.png", SPRITE_SCALING_ENEMY, position_list)


        #Set enemy initial position
        enemy.center_x = 225
        enemy.center_y = 500

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
        arcade.start_render()
        self.clear()
        self.enemy_list.draw()
        self.user.draw()

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

