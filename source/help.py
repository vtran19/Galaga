import arcade
from source import start

class InstructionsView(arcade.View):
    def on_show_view(self):
        arcade.set_background_color(arcade.csscolor.BLACK)
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        self.clear()
        # arcade.draw_text("text", x-location, y-location, arcade.color.TEXTCOLOR, font size, font name)
        arcade.draw_text("How to Play: ", 200, 750, arcade.color.WHITE, 40, font_name="Kenney Pixel")
        # TODO: Write the instructions and rules for the game
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