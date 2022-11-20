import arcade
import sqlite3
from sqlite3 import Error
from source import start
from source import constants as c
from source import play
from datetime import date

class GameOverView(arcade.View):

    def __init__(self):
        super().__init__()

    def setup(self):
        self.user_name = ""

    def on_show_view(self):
        arcade.set_background_color(arcade.csscolor.BLACK)
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        self.clear()
        # arcade.draw_text("text", x-location, y-location, arcade.color.TEXTCOLOR, font size, font name)
        arcade.draw_text("GAME OVER", 150, 500, arcade.color.BLUE_GREEN, 40, font_name="Kenney Blocks")
        arcade.draw_text("Enter name (< 20 characters, press enter when done):", 20, 400, arcade.color.WHITE, 25, font_name="Kenney Pixel")
        arcade.draw_text(self.user_name, 100, 200, arcade.color.WHITE, 25, font_name="Kenney Pixel")


    def on_key_press(self, key):
        if len(self.user_name) < 20:
            self.user_name += key
        elif key == arcade.key.BACKSPACE and len(self.user_name) > 0:
            self.user_name = self.user_name[:-1]
        elif key == arcade.key.ENTER and len(self.user_name) > 0:
            # add data to db and return to home
            db = "galaga_high_scores.db"
            connection = None
            today = date.today()
            
            # exception handling for opening files
            try:
                # connect to the database file or create it if it doesn't exist
                connection = sqlite3.connect(db)

                # database cursor
                cursor = connection.cursor()

                # add naem, score, and date to database
                add_score = 'INSERT INTO HighScores VALUES({},{},{});'.format(self.user_name, play.score, today)
                cursor.execute(add_score)

            except Error as e:
                print(e)

            finally:
                if connection:
                    connection.close()
            start_view = start.StartView()
            start_view.setup()
            self.window.show_view(start_view)
