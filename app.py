from source import constants as c
import arcade
from source import start

def main():
    """
        Main Function to run Galaga game
    """
    # Set up windows and run program
    window = arcade.Window(c.SCREEN_WIDTH, c.SCREEN_HEIGHT, c.SCREEN_TITLE)
    start_view = start.StartView()
    start_view.setup()
    window.show_view(start_view)
    arcade.run()

main() 
