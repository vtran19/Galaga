from source import sprites
import arcade
import random
import soundfile
from source import constants as c
from source import over


class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        # Timer initialization
        self.total_time = 0.0
        self.enemy_timer = 0.0
        self.timer_text = arcade.Text(
            text="00:00:00",
            start_x=c.SCREEN_WIDTH - 50,
            start_y=c.SCREEN_HEIGHT - 25,
            color=arcade.color.WHITE,
            font_size=15,
            anchor_x="center",
        )

        # Score initialization
        self.score = 0

        # boolean for enemies being initialized
        self.initialized = False

        # Empty Lists
        self.user_list = None
        self.user_explosion_list = None
        self.bug_list = None
        self.butterfly_list = None
        self.enemy_explosion_list = None
        self.background_sprite_list = None
        self.lives = None
        self.user_pellet_list = None
        self.enemy_pellet_list = None

        # Set background color
        self.background_color = arcade.color.BLACK

        # User explosion animation frames
        self.user_explosion_texture_list = []
        for index in range(c.USER_LOWER_FRAME_BOUND, c.USER_UPPER_FRAME_BOUND):
            for loops in range(c.USER_FRAME_SPEED):
                self.user_explosion_texture_list.append(arcade.load_texture("./resources/images/user/ship_explosion" +
                                                                            str(index) + ".png"))

        # Enemy explosion animation frames
        self.enemy_explosion_texture_list = []
        for index in range(c.ENEMY_LOWER_FRAME_BOUND, c.ENEMY_UPPER_FRAME_BOUND):
            for loops in range(c.ENEMY_FRAME_SPEED):
                self.enemy_explosion_texture_list.append(arcade.load_texture("./resources/images/enemy/enemy_explosion"
                                                                             + str(index) + ".png"))

        # Load sounds from Pixabay 
        shoot_file_path = "./resources/sounds/shoot_sound.wav"
        explosion_file_path = "./resources/sounds/explosion.wav"

        # Read and rewrite the file with soundfile
        data, samplerate = soundfile.read(shoot_file_path)
        soundfile.write(shoot_file_path, data, samplerate)
        

        self.shoot_sound = arcade.load_sound(shoot_file_path)
        
        data, samplerate = soundfile.read(explosion_file_path)
        soundfile.write(explosion_file_path, data, samplerate)

        self.user_explosion_sound = arcade.load_sound(explosion_file_path)

    def setup(self):
        # User
        user = sprites.User("./resources/images/user/user_ship.png", c.SPRITE_SCALE_USER)
        self.user_list = arcade.SpriteList()
        self.user_list.append(user)

        # User and Enemy Explosion
        self.user_explosion_list = arcade.SpriteList()
        self.enemy_explosion_list = arcade.SpriteList()

        # Lives
        self.lives = arcade.SpriteList()
        lives_position = [25, 20]
        for i in range(0, 3):
            life = sprites.Lives("./resources/images/user/user_ship.png", c.SPRITE_SCALE_LIVES, lives_position)
            lives_position[0] += 25
            self.lives.append(life)

        # Timer
        self.total_time = 0.0

        # Score
        self.score = 0

        # Enemy sprites
        self.bug_list = arcade.SpriteList()
        self.butterfly_list = arcade.SpriteList()
        self.user_pellet_list = arcade.SpriteList()
        self.enemy_pellet_list = arcade.SpriteList()
        # boolean for enemies being initialized
        self.initialized = False
        GameView.setup_enemies(self)

        # Background Sprites
        self.background_sprite_list = []
        for i in range(c.BACKGROUND_SPRITE_FREQ):
            background_sprite = sprites.BackgroundSprite()
            background_sprite.x = random.randrange(c.SCREEN_WIDTH)
            background_sprite.y = random.randrange(c.SCREEN_HEIGHT + 200)
            self.background_sprite_list.append(background_sprite)

    def setup_enemies(self):
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

    def on_update(self, delta_time):
        # get total time
        self.total_time += delta_time
        self.enemy_timer += delta_time

        # Calculate minutes
        minutes = int(self.total_time) // 60

        # Calculate seconds by using a modulus (remainder)
        seconds = int(self.total_time) % 60

        # Calculate 100s of a second
        seconds_100s = int((self.total_time - seconds)*100)

        # format timer
        self.timer_text.text = f"{minutes:02d}:{seconds:02d}:{seconds_100s:02d}"

        #enemies initializing based on how much time has passed
        seconds_100s_elapsed = int((self.enemy_timer - (int(self.enemy_timer) % 60))*100)+(100*(int(self.enemy_timer) % 60))
        if(seconds_100s_elapsed < c.ENEMY_UPDATE_INTERVAL * len(self.bug_list)):
            #update number of enemies based on how much time has passed
            num_updating = seconds_100s_elapsed//c.ENEMY_UPDATE_INTERVAL
            #for loop that updates enemies staggerdly
            for i in range(num_updating):
                self.bug_list[i].update()
                self.butterfly_list[i].update()
        else:
            self.initialized = True

        self.user_list.update()
        self.user_explosion_list.update()
        self.bug_list.update()
        self.butterfly_list.update()
        self.enemy_explosion_list.update()
        for background_sprite in self.background_sprite_list:
            background_sprite.y -= c.BACKGROUND_SPRITE_SPEED * delta_time
            if background_sprite.y < 0:
                background_sprite.reset_pos()

        #if all enemies have been initialized, update enemy lists
        if(self.initialized):
            self.bug_list.update()
            self.butterfly_list.update()

        # Loop through each pellet the user shot
        for pellet in self.user_pellet_list:
            # Checks to see if the bullet has hit any bugs by index
            for i in range(len(self.bug_list)):
                colliding = arcade.check_for_collision(pellet, self.bug_list[i])
                if(colliding):
                    # Enemy explosion animation
                    enemy_explosion = sprites.EnemyExplosionAnimation(self.enemy_explosion_texture_list)
                    enemy_explosion.center_x = self.bug_list[i].center_x
                    enemy_explosion.center_y = self.bug_list[i].center_y
                    enemy_explosion.update()
                    self.enemy_explosion_list.append(enemy_explosion)
                    # Remove pellet and bug, add to score
                    pellet.remove_from_sprite_lists()
                    self.bug_list[i].remove_from_sprite_lists()
                    self.score += 200
                    break

            # Checks to see if the bullet has hit any butterflies by index
            for i in range(len(self.butterfly_list)):
                colliding = arcade.check_for_collision(pellet, self.butterfly_list[i])
                if(colliding):
                    # Enemy explosion animation
                    enemy_explosion = sprites.EnemyExplosionAnimation(self.enemy_explosion_texture_list)
                    enemy_explosion.center_x = self.butterfly_list[i].center_x
                    enemy_explosion.center_y = self.butterfly_list[i].center_y
                    enemy_explosion.update()
                    self.enemy_explosion_list.append(enemy_explosion)
                    # Remove pellet and butterfly sprites, add to score
                    pellet.remove_from_sprite_lists()
                    self.butterfly_list[i].remove_from_sprite_lists()
                    self.score += 500
                    break
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

        # Loop through each pellet the enemies have shot
        for pellet in self.enemy_pellet_list:
            #checks to see if pellet has hit the user
            colliding = arcade.check_for_collision_with_list(pellet,self.user_list)
            if colliding and self.user_list[0].alive:
                # Activate explosion animation sprite and make player is not alive
                GameView.spawn_user_explosion(self)
                self.user_list[0].alive = False
                # Remove a life
                self.lives.remove(self.lives[len(self.lives) - 1])

        # Loop through each bug to see if it's hitting the user
        for bug in self.bug_list:
            # Checks to see if the bug hit the user
            colliding_with_user = arcade.check_for_collision_with_list(bug, self.user_list)
            if len(colliding_with_user) > 0 and self.user_list[0].alive:
                # Activate explosion animation sprite and make player is not alive
                GameView.spawn_user_explosion(self)
                self.user_list[0].alive = False
                # Remove a life
                self.lives.remove(self.lives[len(self.lives) - 1])

        # Loop through each butterfly to see if it's hitting the user
        for but in self.butterfly_list:
            # Checks to see if the butterfly hit the user
            colliding_with_user = arcade.check_for_collision_with_list(but, self.user_list)
            if len(colliding_with_user) > 0 and self.user_list[0].alive:
                # Activate explosion animation sprite and make player is not alive
                GameView.spawn_user_explosion(self)
                self.user_list[0].alive = False
                # Remove a life
                self.lives.remove(self.lives[len(self.lives) - 1])

        # if no lives remain, go to end game menu
        if len(self.lives) < 1:
            end_view = over.GameOverView()
            end_view.setup()
            self.window.show_view(end_view)

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
            #create 3 pellets when enemy begins to dive
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

        #if butterfly and bug lists are empty, spawn more enemies
        if(not(self.butterfly_list) and not(self.bug_list)):
            #set enemy timer = 0 every time enemy lists are both empty
            GameView.setup_enemies(self)
            self.enemy_timer = 0.0
        #update pellets
        self.user_pellet_list.update()
        self.enemy_pellet_list.update()

    def spawn_user_explosion(self):
        user_explosion = sprites.UserExplosionAnimation(self.user_explosion_texture_list)
        user_explosion.center_x = self.user_list[0].center_x
        user_explosion.center_y = self.user_list[0].center_y
        user_explosion.update()
        self.user_explosion_list.append(user_explosion)
        arcade.play_sound(self.user_explosion_sound, c.USER_EXPLOSION_VOL)

    def on_draw(self):
        arcade.start_render()
        self.clear()
        for background_sprite in self.background_sprite_list:
            arcade.draw_point(background_sprite.x, background_sprite.y, background_sprite.color, c.BACKGROUND_SPRITE_SIZE)
        self.timer_text.draw()
        self.bug_list.draw()
        self.butterfly_list.draw()
        self.user_explosion_list.draw()
        self.enemy_explosion_list.draw()
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

    def on_key_press(self, key):
        # If the player presses a key, update the speed
        if key == arcade.key.LEFT:
            self.user_list[0].change_x = -c.USER_SPEED
        elif key == arcade.key.RIGHT:
            self.user_list[0].change_x = c.USER_SPEED
        elif key == arcade.key.SPACE:
            if self.user_list[0].alive:
                # Play shooting sound
                arcade.play_sound(self.shoot_sound, c.PELLET_VOL)
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
