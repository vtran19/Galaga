import arcade
from source import start
import sqlite3
import os
from sqlite3 import Error
from tabulate import tabulate



class ScoreView(arcade.View):
    def on_show_view(self):
        arcade.set_background_color(arcade.csscolor.BLACK)
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        self.clear()
        # arcade.draw_text("text", x-location, y-location, arcade.color.TEXTCOLOR, font size, font name)
        arcade.draw_text("High Scores", 90, 650, arcade.color.BLUE_GREEN, 40, font_name="Kenney Blocks")
        
        scores = self.get_high_score()
        y_position = 600
        for row in scores:
            x_position = 60
            i = 0
            for col in row:
                if i == 1:
                    arcade.draw_text(col, x_position, y_position, arcade.color.GREEN, 20, font_name="Kenney Pixel")
                    x_position += 200
                else:
                    arcade.draw_text(col, x_position, y_position, arcade.color.GREEN, 20, font_name="Kenney Pixel")
                    x_position += 90
                i += 1
            y_position -= 50

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
    
    def get_high_score(self):
        db = "./galaga_high_scores.db"
        connection = None
        scores = None

        # exception handling for opening files
        try:
            # connect to the database file or create it if it doesn't exist
            connection = sqlite3.connect(db)

            # database cursor
            cursor = connection.cursor()

            # get top 10 scores from existing db
            get_scores = 'SELECT ROW_NUMBER () OVER ( ORDER BY score DESC) rownum, user_name, score, date FROM HighScores LIMIT 10;'
            scores = cursor.execute(get_scores)
            scores = cursor.fetchall()
            

        except Error as e:
            print(e)

        finally:
            if connection:
                connection.close()

        return scores

