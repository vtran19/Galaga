import arcade
from source import start
from source import constants as c

class InstructionsView(arcade.View):
    def __init__(self):
        super().__init__()

        # List for arrow key icons
        self.keys_list = None

        # Variables for arrow keys, space bar, and spaceship icon
        self.arrows = None
        self.space = None
        self.spaceship = None



    def on_show_view(self):
        arcade.set_background_color(arcade.csscolor.BLACK)
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def setup(self):
        # Create arrow keys list
        self.keys_list = arcade.SpriteList()

        # Set up keys made from scratch in Canva
        self.arrows = arcade.Sprite("./resources/images/start/arrows.png", c.KEY_SCALE)
        self.arrows.center_x = 300
        self.arrows.center_y = 625
        self.keys_list.append(self.arrows)

        self.space = arcade.Sprite("./resources/images/start/spacebar.png", c.KEY_SCALE)
        self.space.center_x = 300
        self.space.center_y = 475
        self.keys_list.append(self.space)

        self.spaceship = arcade.Sprite("./resources/images/user/user_ship.png", c.SHIP_IMAGE_SCALE)
        self.spaceship.center_x = 300
        self.spaceship.center_y = 300
        self.keys_list.append(self.spaceship)

    def on_draw(self):
        self.clear()

        # Title
        arcade.draw_text("How to Play: ", 200, 750, arcade.color.WHITE, 40, font_name="Kenney Pixel")

        # Game instructions
        self.keys_list.draw()
        arcade.draw_text("Use LEFT and RIGHT arrow keys to move ship side to side", 75, 550, arcade.color.WHITE, 20, font_name = "Kenney Pixel")
        arcade.draw_text("Press space to shoot enemies", 175, 400, arcade.color.WHITE, 20, font_name="Kenney Pixel")
        arcade.draw_text("Collect points by hitting enemies", 160, 225, arcade.color.WHITE, 20, font_name="Kenney Pixel")
        arcade.draw_text("GAME OVER after 3 lives are lost", 160, 190, arcade.color.WHITE, 20, font_name="Kenney Pixel")
        arcade.draw_text("GOOD LUCK!", 230, 150, arcade.color.WHITE, 30, font_name="Kenney Pixel")

        # TODO: Make a default font global variable and default font size (20)

        arcade.draw_text("Press R to Return to Main Menu", 20, 50, arcade.color.WHITE, 30, font_name="Kenney Pixel")
        arcade.draw_text("Press Q to Quit", 20, 20, arcade.color.WHITE, 30, font_name="Kenney Pixel")

    def on_key_press(self, key, modifiers):
        # Starts Menu
        if key == arcade.key.R:
            start_view = start.StartView()
            start_view.setup()
            self.window.show_view(start_view)
        # Quit
        elif key == arcade.key.Q:
            arcade.close_window()