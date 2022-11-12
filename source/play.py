from source import sprites
import arcade
import random
from source import constants as c


class GameView(arcade.View):
    def __init__(self):
        # Call the parent class initializer
        super().__init__()

        # Timer initialization
        self.total_time = 0.0
        self.timer_text = arcade.Text(
            text="00:00:00",
            start_x=c.SCREEN_WIDTH - 425,
            start_y=c.SCREEN_HEIGHT - 20,
            color=arcade.color.WHITE,
            font_size=15,
            anchor_x="center",
        )

        # Score initialization
        self.score = 0

        #boolean for enemies being initialized
        self.initialized = False
        # Initialize sprites
        # Empty Lists are made
        self.user_list = None
        self.bug_list = None
        self.butterfly_list = None
        self.background_sprite_list = None

        self.lives = None
        self.user_pellet_list = None
        self.enemy_pellet_list = None
        # Set background color
        self.background_color = arcade.color.BLACK

    def setup(self):
        # Setup the user
        user = sprites.User("./resources/images/user/user_ship.png", c.SPRITE_SCALE_USER)
        self.user_list = arcade.SpriteList()
        # Append user to user list
        self.user_list.append(user)

        # Setup Lives
        self.lives = arcade.SpriteList()

        # Setup timer
        self.total_time = 0.0

        # Keep track of score

        self.score = 0
        # Set up the user
        # self.user = sprites.User("./resources/images/user/user_ship.png", c.SPRITE_SCALE_USER)

        # Enemy sprites
        self.bug_list = arcade.SpriteList()
        self.butterfly_list = arcade.SpriteList()
        self.user_pellet_list = arcade.SpriteList()
        self.enemy_pellet_list = arcade.SpriteList()

        #boolean for enemies being initialized
        self.initialized = False

        #List of points the bugs will travel too
        idle_position_list_bug = [[25,550],
                            [75,550]]
        init_position_bug = [300.0,850.0]
        #Create bugs
        for i in range(0, c.SCREEN_WIDTH - 50, 50):
            temp_pos_list = []
            for point in idle_position_list_bug:
                temp_pos_list.append([point[0]+40, point[1]])
            idle_position_list_bug = temp_pos_list
            enemy = sprites.Enemy("./resources/images/enemy/bug.png", c.SPRITE_SCALING_BUG, idle_position_list_bug, diving_coefficients=[
                    #movement coefficients are passed to calculate_curve_point as constants that determine the movement of the enemy; all of these numbers
                    #were found mostly through trial and error
                    [[idle_position_list_bug[0][0] + 110.0, idle_position_list_bug[0][1]],[idle_position_list_bug[0][0] + 110.0, -30.0],[idle_position_list_bug[0][0] + 90.0, idle_position_list_bug[0][1]],[idle_position_list_bug[0][0] - 110.0, -30.0]],
                    [[idle_position_list_bug[0][0] - 90.0, -30.0],[idle_position_list_bug[0][0] + 90.0, 200.0],[idle_position_list_bug[0][0] - 90.0 , 425.0],[idle_position_list_bug[0][0]-150.0, 600.0]],
                    [[idle_position_list_bug[0][0]-150.0, 600.0],[idle_position_list_bug[0][0]-25.0, 850.0],[idle_position_list_bug[0][0]+165.0,700.0],[idle_position_list_bug[0][0],idle_position_list_bug[0][1]]]],
                    #init coefficients passed to calculate_curve_point to give enemies some initial movement before they start diving
                    init_coefficients=[
                        [[init_position_bug[0], init_position_bug[1]],[init_position_bug[0]-150.0,init_position_bug[1]-175.0],[init_position_bug[0]-375.0,init_position_bug[1]-150.0],[init_position_bug[0]-190.0,init_position_bug[1]-325.0]],
                        [[init_position_bug[0]-190.0,init_position_bug[1]-325.0],[init_position_bug[0]-50.0,init_position_bug[1]-301.0],[init_position_bug[0]+150.0,init_position_bug[1]-275.0],[init_position_bug[0]+350.0,init_position_bug[1]-325.0]],
                        [[init_position_bug[0]+350.0,init_position_bug[1]-325.0], [init_position_bug[0]+150.0,init_position_bug[1]-350.0],[init_position_bug[0],init_position_bug[1]-325.0],[idle_position_list_bug[0][0],idle_position_list_bug[0][1]]]
                    ])
                    #need to find a more elegant way to place these^^

            #Set enemy initial position
            enemy.center_x = init_position_bug[0]
            enemy.center_y = init_position_bug[1]

            #append enemy to bug_list
            self.bug_list.append(enemy)

        #List of points the butterflies will travel too
        idle_position_list_but = [[25,650],
                                [75,650]]
        init_position_but = [300.0,950.0]
        #Create butterflies
        for i in range(0, c.SCREEN_WIDTH - 50, 50):
            temp_pos_list = []
            for point in idle_position_list_but:
                temp_pos_list.append([point[0]+40, point[1]])
            idle_position_list_but = temp_pos_list
            enemy = sprites.Butterfly("./resources/images/enemy/butterfly.png", c.SPRITE_SCALING_BUTTERFLY, idle_position_list_but, diving_coefficients=[
                    #movement coefficients are passed to calculate_curve_point as constants that determine the movement of the enemy; all of these numbers
                    #were found mostly through trial and error
                    [[idle_position_list_but[0][0] + 110.0, idle_position_list_but[0][1]],[idle_position_list_but[0][0] + 110.0, -30.0],[idle_position_list_but[0][0] + 90.0, idle_position_list_but[0][1]],[idle_position_list_but[0][0] - 110.0, -30.0]],
                    [[idle_position_list_but[0][0] - 90.0, -30.0],[idle_position_list_but[0][0] + 90.0, 200.0],[idle_position_list_but[0][0] - 90.0 , 425.0],[idle_position_list_but[0][0]-150.0, 600.0]],
                    [[idle_position_list_but[0][0]-150.0, 600.0],[idle_position_list_but[0][0]-25.0, 850.0],[idle_position_list_but[0][0]+165.0,700.0],[idle_position_list_but[0][0],idle_position_list_but[0][1]]]],
                    init_coefficients=[
                        [[init_position_but[0], init_position_but[1]],[init_position_but[0]-150.0,init_position_but[1]-175.0],[init_position_but[0]-375.0,init_position_but[1]-150.0],[init_position_but[0]-190.0,init_position_but[1]-325.0]],
                        [[init_position_but[0]-190.0,init_position_but[1]-325.0],[init_position_but[0]-50.0,init_position_but[1]-301.0],[init_position_but[0]+150.0,init_position_but[1]-275.0],[init_position_but[0]+350.0,init_position_but[1]-325.0]],
                        [[init_position_but[0]+350.0,init_position_but[1]-325.0], [init_position_but[0]+150.0,init_position_but[1]-350.0],[init_position_but[0],init_position_but[1]-325.0],[idle_position_list_but[0][0],idle_position_list_but[0][1]]]
                    ])

            #Set enemy initial position
            enemy.center_x = init_position_but[0]
            enemy.center_y = init_position_but[1]

            #append enemy to butterfly_list
            self.butterfly_list.append(enemy)

        # Create Lives
        lives_position = [25, 20]
        for i in range(0, 3):
            life = sprites.Lives("./resources/images/user/user_ship.png", c.SPRITE_SCALE_LIVES, lives_position)
            lives_position[0] += 25
            self.lives.append(life)

        # Background Sprites
        self.background_sprite_list = []
        for i in range(c.BACKGROUND_SPRITE_FREQ):
            background_sprite = sprites.BackgroundSprite()
            background_sprite.x = random.randrange(c.SCREEN_WIDTH)
            background_sprite.y = random.randrange(c.SCREEN_HEIGHT + 200)
            self.background_sprite_list.append(background_sprite)

    def on_update(self, delta_time):
        # get total time
        self.total_time += delta_time

        # Calculate minutes
        minutes = int(self.total_time) // 60

        # Calculate seconds by using a modulus (remainder)
        seconds = int(self.total_time) % 60

        #calculate 100s of a second
        seconds_100s = int((self.total_time - seconds)*100)
        
        # format timer
        self.timer_text.text = f"{minutes:02d}:{seconds:02d}:{seconds_100s:02d}"

        self.user_list.update()

        #enemies initializing based on how much time has passed
        seconds_100s_elapsed = seconds_100s+(100*seconds)
        if(seconds_100s_elapsed < c.ENEMY_UPDATE_INTERVAL * len(self.bug_list)):
            #update number of enemies based on how much time has passed
            num_updating = seconds_100s_elapsed//c.ENEMY_UPDATE_INTERVAL
            for i in range(num_updating):
                self.bug_list[i].update()
                self.butterfly_list[i].update()
        else:
            self.initialized = True
        
        for background_sprite in self.background_sprite_list:
            background_sprite.y -= c.BACKGROUND_SPRITE_SPEED * delta_time
            if background_sprite.y < 0:
                background_sprite.reset_pos()
        self.user_pellet_list.update()
        self.enemy_pellet_list.update()

        #check if any bugs are diving or if all bugs are still being initialized
        diving = False
        init = True
        for enemy in self.bug_list:
            if(enemy.diving):
                diving = True
            if(not(enemy.init)):
                init = False

        #if no bugs are diving and all bugs have been initialzied, assign a bug to dive
        if(not(diving) and not(init)):
            #find a random bug
            index = random.randint(0,len(self.bug_list)-1)
            #set diving = true and create enemy pellets
            self.bug_list[index].diving = True
            for i in range (int(self.bug_list[index].center_x) - 30,int(self.bug_list[index].center_x) +30 ,29):
                pellet = arcade.Sprite("./resources/images/pellet.png", c.SPRITE_SCALE_PELLET)                    
                pellet.change_y = -c.PELLET_SPEED

                #put pellet in postion such that enemy shoots 3 evenly spaced pellets
                pellet.center_x = i
                pellet.bottom = self.bug_list[index].bottom

                #append to enemy list
                self.enemy_pellet_list.append(pellet)

        #check if any butterflies are diving or if all butterflies have been initialized
        diving = False
        init = True
        for enemy in self.butterfly_list:
            if(enemy.diving):
                diving = True
            if(not(enemy.init)):
                init = False

        #if no butterflies are diving, randomly assign an enemy to dive
        if(not(diving) and not(init)):
            #find a random butterfly
            index = random.randint(0,len(self.butterfly_list)-1)
            self.butterfly_list[index].diving = True
            #create enemy pellets
            for i in range (int(self.butterfly_list[index].center_x) -30,int(self.butterfly_list[index].center_x) + 30, 29):
                pellet = arcade.Sprite("./resources/images/pellet.png", c.SPRITE_SCALE_PELLET)
                pellet.change_y = -c.PELLET_SPEED

                #put pellet in postion such that enemy shoots 3 evenly spaced pellets
                pellet.center_x = i
                pellet.bottom = self.butterfly_list[index].bottom

                #append to enemy list
                self.enemy_pellet_list.append(pellet)
        
        if(self.initialized):
            self.bug_list.update()
            self.butterfly_list.update()
    
        # Loop through each pellet the user shot
        for pellet in self.user_pellet_list:

            # Checks to see if the bullet hit the enemies
            colliding_with_bug = arcade.check_for_collision_with_list(pellet, self.bug_list)
            colliding_with_butterfly = arcade.check_for_collision_with_list(pellet, self.butterfly_list)
            
            if len(colliding_with_bug or colliding_with_butterfly) > 0:
                # Removes bullet if hit enemy
                pellet.remove_from_sprite_lists()

                # Adds to score
                self.score += 200

            # Removes bullet if off screen
            if pellet.bottom > c.SCREEN_HEIGHT:
                pellet.remove_from_sprite_lists()

        # Loop through each bug to see if it's hitting the user
        for bug in self.bug_list:
            # Checks to see if the bug hit the user
            colliding_with_user = arcade.check_for_collision_with_list(bug, self.user_list)
            if len(colliding_with_user) > 0:
                # User is not alive if hit
                self.user_list[0].alive = False

    def on_draw(self):
        arcade.start_render()
        self.clear()
        for background_sprite in self.background_sprite_list:
            arcade.draw_point(background_sprite.x, background_sprite.y, background_sprite.color, c.BACKGROUND_SPRITE_SIZE)
        self.timer_text.draw()
        self.bug_list.draw()
        self.butterfly_list.draw()
        # Only draw the user if they are alive
        if self.user_list[0].alive:
            self.user_list.draw()
        self.lives.draw()
        self.user_pellet_list.draw()
        self.enemy_pellet_list.draw()

        # Draw score
        score_text = "Score: " + str(self.score)
        arcade.draw_text(
            score_text,
            10,
            (c.SCREEN_HEIGHT - 25),
            arcade.color.WHITE,
            15
        )

        # Prompt user to respawn when alive=False, removes life from bottom
        if not self.user_list[0].alive:
            arcade.draw_text("press space to respawn", 200, 200, arcade.color.WHITE, 20, font_name="Kenney Pixel")

    def on_key_press(self, key, modifiers):
        # If the player presses a key, update the speed
        if key == arcade.key.LEFT:
            self.user_list[0].change_x = -c.USER_SPEED
        elif key == arcade.key.RIGHT:
            self.user_list[0].change_x = c.USER_SPEED
        elif key == arcade.key.SPACE:
            if self.user_list[0].alive:
                # Create a pellet
                pellet = arcade.Sprite("./resources/images/pellet.png", c.SPRITE_SCALE_PELLET)

                # Set pellet speed
                pellet.change_y = c.PELLET_SPEED

                # Puts pellet in position of user
                pellet.center_x = self.user_list[0].center_x
                pellet.bottom = self.user_list[0].top

                # Add pellet to list
                self.user_pellet_list.append(pellet)
            else:
                # Spawns in user again, alive, in the center
                self.user_list[0].left = 325
                self.user_list[0].right = 325
                self.user_list[0].top = 65
                self.user_list[0].bottom = 35
                self.user_list[0].alive = True

        elif key == arcade.key.Q:
            arcade.close_window()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.user_list[0].change_x = 0