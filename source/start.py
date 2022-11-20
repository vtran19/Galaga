import arcade
from source import constants as c
import random
from source import sprites
from source import play
from source import help
from source import score
import soundfile

class StartView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_sprite_list = None

        file_path = "./resources/sounds/theme_song.wav"

        # Read and rewrite the file with soundfile
        data, samplerate = soundfile.read(file_path)
        soundfile.write(file_path, data, samplerate)

        # Load theme song
        self.theme_song = arcade.load_sound(file_path)

        # Play theme song
        self.media_player = self.theme_song.play()


    def on_show_view(self):
        arcade.set_background_color(arcade.csscolor.BLACK)
        # to reset the viewport
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def setup(self):
        # Background Sprites
        self.background_sprite_list = []
        for i in range(c.BACKGROUND_SPRITE_FREQ):
            background_sprite = sprites.BackgroundSprite()
            background_sprite.x = random.randrange(c.SCREEN_WIDTH)
            background_sprite.y = random.randrange(c.SCREEN_HEIGHT + 200)
            self.background_sprite_list.append(background_sprite)

    def on_update(self, delta_time):
        for background_sprite in self.background_sprite_list:
            background_sprite.y -= c.BACKGROUND_SPRITE_SPEED * delta_time
            if background_sprite.y < 0:
                background_sprite.reset_pos()

    def on_draw(self):
        self.clear()
        # Background Sprites
        for background_sprite in self.background_sprite_list:
            arcade.draw_point(background_sprite.x, background_sprite.y, background_sprite.color, c.BACKGROUND_SPRITE_SIZE)
        # Text
        arcade.draw_text("GALAGA", 80, 500, arcade.color.BLUE_GREEN, 80, font_name="Kenney Blocks")
        arcade.draw_text("          Press S to Start\nPress H for High Scores\nPress I for Instructions\n            Press Q to Quit", 160, 450,
                         arcade.color.WHITE, 30, font_name="Kenney Pixel", multiline=True, width=500)

    def on_key_press(self, key, modifiers):
        # Starts game
        if key == arcade.key.S:
            self.media_player.pause()
            game_view = play.GameView()
            game_view.setup()
            self.window.show_view(game_view)
        # High Scores
        elif key == arcade.key.H:
            score_view = score.ScoreView()
            self.window.show_view(score_view)
        # Instructions
        elif key == arcade.key.I:
            self.media_player.pause()
            instructions_view = help.InstructionsView()
            instructions_view.setup()
            self.window.show_view(instructions_view)
        # Quit
        elif key == arcade.key.Q:
            arcade.close_window()

