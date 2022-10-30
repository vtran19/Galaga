from operator import truediv
from re import U
from tokenize import Pointfloat
import arcade
import os
import math
import random
from time import perf_counter


SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Galaga"
SPRITE_SCALE_USER = 0.04
USER_SPEED = 3.0
#Movement Constants
UNIT_VECTOR_UP = [0.0,1.0]
UNIT_VECTOR_DOWN = [0.0,-1.0]
#Enemy Constants
SPRITE_SCALING_ENEMY = 2
ENEMY_SPEED = 1
ENEMY_INITIAL_SPACING = 25
# Pellet Constants
PELLET_SPEED = 5
SPRITE_SCALE_PELLET = .07
class Enemy(arcade.Sprite):
    """
        Class to represent enemies on the screen. Likely to split up into more than one class
        later to reflect different enemy types
    """
    def __init__(self, image, scale, position_list, movement_coefficients):
        # timer for enemy lifespan related to movement, start timer
        #self.start_time = perf_counter()
        # when should the enemy randomly dive 
        #self.dive_time = random.uniform(self.start_time + 10, self.start_time + 60)
        # dive x location, needs to remain constant 
        #self.dive_dest = [random.randint(0, 450), -20]

        super().__init__(image, scale)
        self.position_list = position_list
        self.cur_position = 0
        self.speed = ENEMY_SPEED
        self.movement_coefficients = movement_coefficients
        self.movement_variable = 0.01
        self.diving = False

    def calculate_curve_point(self):
        #define bezeir curve variables
        t = self.movement_variable
        tt = self.movement_variable ** 2
        ttt = t * tt
        u = 1.0 - t
        uu = u * u
        uuu = uu * u

        #calculate point on curve based on self.movement_coefficients
        point_x = (uuu * self.movement_coefficients[0][0]) + (3*uu*t* self.movement_coefficients[1][0]) + (3*u*tt* self.movement_coefficients[2][0]) + (ttt* self.movement_coefficients[3][0])
        point_y = (uuu * self.movement_coefficients[0][1]) + (3*uu*t* self.movement_coefficients[1][1]) + (3*u*tt* self.movement_coefficients[2][1]) + (ttt* self.movement_coefficients[3][1])

        #update movement_variable (t) 
        self.movement_variable += .01
        if self.movement_variable > 1.0:
            self.movement_variable = .01

        #return point
        return [point_x, point_y]

    def update(self):
        """Make enemies follow a path. To start, enemies move side to side"""
        #Start location
        start_x = self.center_x
        start_y = self.center_y

        if(self.diving):
            #call calculate_curve_point for enemy if moving along curve
            next_point = Enemy.calculate_curve_point(self)

            self.center_x = next_point[0]
            self.center_y = next_point[1]

            if(self.center_x == self.position_list[0][0] and self.center_y == self.position_list[0][1]):
                self.diving = False
        else: #Idle Movement
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
            if distance <= speed:
                self.cur_position += 1
                if self.cur_position >= len(self.position_list):
                    self.cur_position = 0

class User(arcade.Sprite):
    """ User Class """
    def __init__(self, image, scale):
        super().__init__(image, scale)
        self.change_x = 0
        self.change_y = 0
        self.left = 325
        self.right = 325
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



class Game(arcade.Window):
    def __init__(self, width, height, title):
        # Call the parent class initializer
        super().__init__(width, height, title)

        # Timer initialization
        self.total_time = 0.0
        self.timer_text = arcade.Text(
            text="00:00:00",
            start_x=SCREEN_WIDTH - 425,
            start_y=SCREEN_HEIGHT - 20,
            color=arcade.color.WHITE,
            font_size=15,
            anchor_x="center",
        )

        # Score initialization
        self.score = 0

        # Initialize sprites
        self.user = None
        self.enemy_list = None
        self.pellet_list = None

        # Set background color
        self.background_color = arcade.color.BLACK

    def setup(self):
        #Set up the user
        self.user = User("./resources/images/user_ship.png", SPRITE_SCALE_USER)

        # Setup timer
        self.total_time = 0.0

        # Keep track of score
        self.score = 0

        #Sprite Lists
        self.enemy_list = arcade.SpriteList()
        self.pellet_list = arcade.SpriteList()

        #List of points the enemy will travel too 
        position_list = [[25,650],
                        [75,650]]
        #Create enemy
        for i in range(0, self.width - 50, 50):
            temp_pos_list = []
            for point in position_list:
                temp_pos_list.append([point[0]+40, point[1]])
            position_list = temp_pos_list
            enemy = Enemy("./resources/images/enemy/bug.png", SPRITE_SCALING_ENEMY, position_list, movement_coefficients=[[position_list[0][0] + 50.0, position_list[0][1]],[position_list[0][0] + 50.0, -20.0],[position_list[0][0] + 50.0, position_list[0][1]],[position_list[0][0] - 50.0, 20.0]])

            #Set enemy initial position
            enemy.center_x = position_list[0][0]
            enemy.center_y = position_list[0][1]

            #append enemy to enemy_list
            self.enemy_list.append(enemy)
                


    def on_update(self, delta_time):
        # get total time 
        self.total_time += delta_time

        # Calculate minutes
        minutes = int(self.total_time) // 60

        # Calculate seconds by using a modulus (remainder)
        seconds = int(self.total_time) % 60

        # format timer
        self.timer_text.text = f"{minutes:02d}:{seconds:02d}"

        self.user.update()
        self.enemy_list.update()
        self.pellet_list.update()

        #check if any enemies are diving
        diving = False
        for enemy in self.enemy_list:
            if(enemy.diving):
                diving = True
        #if no enemies are diving, randomly assign an enemy to dive
        if(not(diving)):
            index = random.randint(0,len(self.enemy_list))
            self.enemy_list[index].diving = True
        
        
        # Loop through each pellet the user shot
        for pellet in self.pellet_list:

            # Checks to see if the bullet hit the enemies
            colliding_with = arcade.check_for_collision_with_list(pellet, self.enemy_list)

            if len(colliding_with) > 0:
                # Removes bullet if hit enemy
                pellet.remove_from_sprite_lists()

                # Adds to score
                self.score += 200
            
            # Removes bullet if off screen
            if pellet.bottom > SCREEN_HEIGHT:
                pellet.remove_from_sprite_lists()

    def on_draw(self):
        arcade.start_render()
        self.clear()
        self.timer_text.draw()
        self.enemy_list.draw()
        self.user.draw()
        self.pellet_list.draw()

        # Draw score
        score_text = "Score: " + str(self.score)
        arcade.draw_text(
            score_text,
            10,
            (SCREEN_HEIGHT - 25),
            arcade.color.WHITE,
            15
        )

    def on_key_press(self, key, modifiers):
        # If the player presses a key, update the speed
        if key == arcade.key.LEFT:
            self.user.change_x = -USER_SPEED
        elif key == arcade.key.RIGHT:
            self.user.change_x = USER_SPEED
        elif key == arcade.key.SPACE:
            # Create a pellet
            pellet = arcade.Sprite("./resources/images/pellet.png", SPRITE_SCALE_PELLET)
            
            # Set pellet speed
            pellet.change_y = PELLET_SPEED

            # Puts pellet in position of user
            pellet.center_x = self.user.center_x
            pellet.bottom = self.user.top

            # Add pellet to list
            self.pellet_list.append(pellet)


    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.user.change_x = 0


def main():

    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


main()

