from game import Game
from settings import Settings

import arcade

if __name__ == '__main__':
    app = Game(
        field_size=Settings.field_sises[1],
        initial_snake_length=Settings.initial_snake_length,
    )
    arcade.run()
