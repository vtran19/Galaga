"""Constants File"""

# Screen Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Galaga"

# Background Constants
BACKGROUND_SPRITE_SPEED = 100
BACKGROUND_SPRITE_FREQ = 120
BACKGROUND_SPRITE_SIZE = 2

# Start instructions constants
KEY_SCALE = 0.75
SHIP_IMAGE_SCALE = .07
TITLE_FONT_SIZE = 40
NORMAL_FONT_SIZE = 20
MENU_FONT_SIZE = 30
FONT = "Kenney Pixel"

# User Constants
SPRITE_SCALE_USER = 0.04
SPRITE_SCALE_LIVES = 0.02
USER_SPEED = 2.0
USER_EXPLOSION_SCALE = 0.15

# Explosion Animations Constants, must be ints
USER_LOWER_FRAME_BOUND = 1
USER_UPPER_FRAME_BOUND = 5
USER_FRAME_SPEED = 4
ENEMY_LOWER_FRAME_BOUND = 1
ENEMY_UPPER_FRAME_BOUND = 6
ENEMY_FRAME_SPEED = 2
ENEMY_EXPLOSION_FRAME_SCALE = 0.1

#Movement Constants
UNIT_VECTOR_UP = [0.0,1.0]
UNIT_VECTOR_DOWN = [0.0,-1.0]


# Enemy Constants
SPRITE_SCALING_BUG = 2.10
SPRITE_SCALING_BUTTERFLY = 2.5
ENEMY_SPEED = 1.25
ENEMY_INITIAL_SPACING = 25
ENEMY_UPDATE_INTERVAL = 25

# Pellet Constants
PELLET_SPEED = 5
SPRITE_SCALE_PELLET = .10

# Sound Constants
USER_EXPLOSION_VOL = 0.1
PELLET_VOL = .2