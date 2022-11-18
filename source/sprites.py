import arcade
from source import constants as c
import math
import random
import time

class Enemy(arcade.Sprite):
    """
        Class to represent enemies on the screen. Likely to split up into more than one class
        later to reflect different enemy types
    """
    def __init__(self, image, scale, position_list, diving_coefficients, init_coefficients):
        # timer for enemy lifespan related to movement, start timer
        #self.start_time = perf_counter()
        # when should the enemy randomly dive 
        #self.dive_time = random.uniform(self.start_time + 10, self.start_time + 60)
        # dive x location, needs to remain constant 
        #self.dive_dest = [random.randint(0, 450), -20]

        super().__init__(image, scale)
        self.position_list = position_list
        self.cur_position = 0
        self.speed = c.ENEMY_SPEED
        self.diving_coefficients = diving_coefficients
        self.init_coefficients = init_coefficients
        self.movement_index = 0
        self.movement_variable = 0.01
        self.diving = False
        self.init = True

    def calculate_curve_point(self):
        #define bezeir curve variables
        t = self.movement_variable
        tt = t ** 2
        ttt = t * tt
        u = 1.0 - t
        uu = u * u
        uuu = uu * u

        if(self.diving):
            #calculate point on curve based on self.diving_coefficients
            point_x = (uuu * self.diving_coefficients[self.movement_index][0][0]) + (3*uu*t* self.diving_coefficients[self.movement_index][1][0]) + (3*u*tt* self.diving_coefficients[self.movement_index][2][0]) + (ttt* self.diving_coefficients[self.movement_index][3][0])
            point_y = (uuu * self.diving_coefficients[self.movement_index][0][1]) + (3*uu*t* self.diving_coefficients[self.movement_index][1][1]) + (3*u*tt* self.diving_coefficients[self.movement_index][2][1]) + (ttt* self.diving_coefficients[self.movement_index][3][1])
        elif(self.init):
            #calculate point on curve based on self.init_coefficients
            point_x = (uuu * self.init_coefficients[self.movement_index][0][0]) + (3*uu*t* self.init_coefficients[self.movement_index][1][0]) + (3*u*tt* self.init_coefficients[self.movement_index][2][0]) + (ttt* self.init_coefficients[self.movement_index][3][0])
            point_y = (uuu * self.init_coefficients[self.movement_index][0][1]) + (3*uu*t* self.init_coefficients[self.movement_index][1][1]) + (3*u*tt* self.init_coefficients[self.movement_index][2][1]) + (ttt* self.init_coefficients[self.movement_index][3][1])

        #update movement_variable (t)
        self.movement_variable += .01
        if self.movement_variable > 1.0:
            self.movement_variable = 0

        #return point
        return [point_x, point_y]

    def update(self):
        """Make enemies follow a path. To start, enemies move side to side"""
        #Start location
        start_x = self.center_x
        start_y = self.center_y

        if(self.init):
            #if movement variable is 0, need to change movement index
            if(self.movement_variable == 0):
                self.movement_index += 1
                #if the index is out of bounds, enemy is no longer being initialized, reset variables for next movement
                if(self.movement_index>=len(self.init_coefficients)):
                    self.init = False
                    self.movement_index = 0
                    self.movement_variable = .01
                    self.angle = 0
                    self.center_x = self.position_list[0][0]
                    self.center_y = self.position_list[0][1]
                    return
            #call calculate_curve_point for enemy if moving along curve
            next_point = Enemy.calculate_curve_point(self)

            #calculate direction that enemy should be facing
            self.angle = math.degrees(math.atan2(next_point[1] - self.center_y, next_point[0]-self.center_x) + 3*math.pi/2)

            #set location
            self.center_x = next_point[0]
            self.center_y = next_point[1]

        elif(self.diving): #Diving Movement
            #if movement variable is 0, need to change movement index
            if(self.movement_variable == 0):
                self.movement_index += 1
                #if the index is out of bounds, enemy is no longer diving, reset variables for next movement
                if(self.movement_index>=len(self.diving_coefficients)):
                    self.diving = False
                    self.movement_index = 0
                    self.movement_variable = .01
                    self.angle = 0
                    self.center_x = self.position_list[0][0]
                    self.center_y = self.position_list[0][1]
                    return    
            #call calculate_curve_point for enemy if moving along curve
            next_point = Enemy.calculate_curve_point(self)

            #calculate direction that enemy should be facing
            self.angle = math.degrees(math.atan2(next_point[1] - self.center_y, next_point[0]-self.center_x) + 3*math.pi/2)

            #set location
            self.center_x = next_point[0]
            self.center_y = next_point[1]
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

class Butterfly(Enemy):
    def __init__(self, image, scale, position_list, diving_coefficients, init_coefficients):
        Enemy.__init__(self, image, scale, position_list, diving_coefficients, init_coefficients)
    
    #eventually overwrite update function to implement butterflies "escorting" galaga enemies
    #def update(self):

class User(arcade.Sprite):
    """ user Class """
    def __init__(self, image, scale):
        super().__init__(image, scale)
        self.change_x = 0
        self.change_y = 0
        self.left = 325
        self.right = 325
        self.top = 65
        self.bottom = 35
        self.alive = True

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
        elif self.right > c.SCREEN_WIDTH - 1:
            self.right = c.SCREEN_WIDTH - 1


class UserExplosionAnimation(arcade.Sprite):
    """ class for user explosion animation sprite """
    def __init__(self, texture_list):
        super().__init__()
        self.current_texture = 0
        self.textures = texture_list
        self.scale = c.SPRITE_SCALE_USER

    def update(self):
        self.current_texture += 1
        if self.current_texture < len(self.textures):
            self.set_texture(self.current_texture)
        else:
            self.remove_from_sprite_lists()


class BackgroundSprite(arcade.Sprite):
    """ Background Sprite Class"""
    def __init__(self):
        super().__init__()
        self.x = 0
        self.y = 0
        self._color = (random.randrange(256), random.randrange(256), random.randrange(256))

    def reset_pos(self):
        self.x = random.randrange(c.SCREEN_WIDTH)
        self.y = random.randrange(c.SCREEN_HEIGHT, c.SCREEN_HEIGHT+100)
        
class Lives(arcade.Sprite):
    """ Lives Sprite Class """
    def __init__(self, image, scale, position):
        super().__init__(image, scale)
        self.center_x = position[0]
        self.center_y = position[1]
        self.lives = 3
    def update(self):
        # Updates the number of lives displayed
        self.lives -= 1
        if self.lives == 0:
            # have it end game
            pass