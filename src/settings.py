import arcade

colour = tuple[int, int, int]


class Settings:
    """Settings class."""

    line_width: int = 2
    cell_size: int = 20

    text_colour: colour = arcade.color.BLACK

    border_symbol: int = 1
    border_colour: colour = arcade.color.LIGHT_BLUE
    cells_colour: colour = arcade.color.BLACK

    snake_symbol: int = 2
    initial_snake_length: int = 3
    snake_alive_colour: colour = arcade.color.LIGHT_GREEN
    snake_dead_colour: colour = arcade.color.LIGHT_GRAY
    snake_eyes_colour: colour = arcade.color.BLACK
    snake_mouth_colour: colour = arcade.color.LIGHT_RED_OCHRE

    apple_symbol: int = 3
    apple_colour: colour = arcade.color.LIGHT_RED_OCHRE
    apple_delay: int = 4

    speed_list: tuple = (
        0.31,
        0.28,
        0.25,
        0.22,
        0.19,
        0.17,
        0.15,
        0.14,
        0.13,
        0.12,
        0.11,
        0.09,
        0.08,
        0.07,
        0.06,
    )

    field_sises: tuple = (
        20,
        25,
        30,
        35,
        40,
    )
