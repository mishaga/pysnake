import arcade

from basics import GameStatus, Point, SnakeDirection
from field import Field
from settings import Settings
from snake import Snake


class Game(arcade.Window):
    """Class of the game.

    Draws all the stuff.
    Controls the game.
    Has link to field.
    """

    field: Field

    def __init__(self, field_size: int, initial_snake_length: int) -> None:
        self._field_size = field_size
        self._initial_snake_length = initial_snake_length
        self._allow_drawing = True
        self._apple_delay_counter = 0

        self._apples = 0
        self._speed = 0
        self._status = GameStatus.READY

        width, height = self.__get_window_scale()
        super().__init__(width=width, height=height, title='PySnake')
        arcade.set_background_color(arcade.color.WHITE)

        self.__create_playground(field_size)

    def on_key_press(self, key: int, modifiers: int) -> None:
        """Catch key press."""
        match self._status:
            case GameStatus.READY:
                match key:
                    case arcade.key.ENTER:
                        self.__action()
                    case arcade.key.KEY_1:
                        self.__create_playground(Settings.field_sises[0])
                    case arcade.key.KEY_2:
                        self.__create_playground(Settings.field_sises[1])
                    case arcade.key.KEY_3:
                        self.__create_playground(Settings.field_sises[2])
                    case arcade.key.KEY_4:
                        self.__create_playground(Settings.field_sises[3])
                    case arcade.key.KEY_5:
                        self.__create_playground(Settings.field_sises[4])
            case GameStatus.ACTION:
                match key:
                    case arcade.key.UP:
                        self.snake.redirect(SnakeDirection.UP)
                    case arcade.key.DOWN:
                        self.snake.redirect(SnakeDirection.DOWN)
                    case arcade.key.LEFT:
                        self.snake.redirect(SnakeDirection.LEFT)
                    case arcade.key.RIGHT:
                        self.snake.redirect(SnakeDirection.RIGHT)
            case GameStatus.OVER:
                if key == arcade.key.ESCAPE:
                    self.__restart()

    def on_update(self, *args, **kwargs) -> None:
        if self._status == GameStatus.ACTION:
            nxt = self.snake.get_next_step()
            if self.field.check_next_step(nxt):
                self.__move_snake(nxt)
            else:
                self.__over()

    def on_draw(self) -> None:
        arcade.start_render()
        if self._allow_drawing:
            self.__draw_cells_net()
            self.__draw_field()
            self.__draw_face()
            self.__draw_stat()

    def __action(self) -> None:
        """Start the game."""
        self._status = GameStatus.ACTION

    def __over(self) -> None:
        """Stop the game."""
        self._status = GameStatus.OVER

    def __create_playground(self, field_size: int) -> None:
        """Create playground of given size.

        While creating playground, it holds drawing functions.
        """
        self._allow_drawing = False

        self._field_size = field_size
        width, height = self.__get_window_scale()
        self.width = width
        self.height = height

        self.__restart()

        self._allow_drawing = True

    def __restart(self) -> None:
        coords = []
        mid = self._field_size // 2
        for i in range(self._initial_snake_length):
            coords.append(Point(mid + i - 1, mid))
        self.snake = Snake(coords)
        self.field = Field(self._field_size, self.snake)

        self._apples = 0
        self._speed = 0
        self._apple_delay_counter = 0
        self._status = GameStatus.READY

        self.set_update_rate(Settings.speed_list[self._speed])

    def __get_window_scale(self) -> tuple[int, int]:
        """By given field_size returns width and height for window."""
        width = Settings.cell_size * (self._field_size + 2)
        height = width + Settings.cell_size * 3
        return width, height

    def __get_cell_center_coords(self, point: Point) -> tuple[float, float]:
        """Return window coords of center of a cell by its coords in the matrix."""
        m = Settings.cell_size
        n = self._field_size
        x = m + point.x * m + m / 2
        y = n * m - (point.y * m - m / 2)
        return x, y

    def __move_snake(self, next_step: Point) -> None:
        """Moving snake to next step. Detect if snake ate apple."""
        if self.field.matrix[next_step.x][next_step.y] == Settings.apple_symbol:
            # ate apple
            self.field.apple = None
            self._apples += 1
            self._apple_delay_counter = 0
            # increase speed, if needed
            if self._speed + 1 < len(Settings.speed_list):
                self._speed += 1
                self.set_update_rate(Settings.speed_list[self._speed])
        else:
            # just move
            tail = self.snake.cut_tail()
            self.field.clear_cell(tail)

        self.snake.move_head(next_step)
        self.field.draw_snake_move(next_step)

        # detect, if new apple needed
        if self.field.apple is None:
            self._apple_delay_counter += 1
            if self._apple_delay_counter == Settings.apple_delay:
                point = self.field.get_random_free_cell()
                self.field.add_apple(Point(point.x, point.y))

    def __draw_cells_net(self) -> None:
        """Draw cells."""
        n = self._field_size
        cell_size = Settings.cell_size
        line_length = cell_size * n

        x, y = cell_size, cell_size
        for i in range(n + 1):
            arcade.draw_line(
                start_x=x,
                start_y=y,
                end_x=x + line_length,
                end_y=y,
                color=Settings.cells_colour,
                line_width=Settings.line_width,
            )
            y += cell_size

        x, y = cell_size, cell_size
        for i in range(n + 1):
            arcade.draw_line(
                start_x=x,
                start_y=y,
                end_x=x,
                end_y=y + line_length,
                color=Settings.cells_colour,
                line_width=Settings.line_width,
            )
            x += cell_size

    def __draw_field(self) -> None:
        """Draw borders, apple and snake (without face)."""
        n = self._field_size
        w = Settings.cell_size - Settings.line_width
        h = Settings.cell_size - Settings.line_width
        what_to_draw = {
            Settings.border_symbol,
            Settings.snake_symbol,
            Settings.apple_symbol,
        }
        colours_map = {
            Settings.border_symbol: Settings.border_colour,
            Settings.snake_symbol: Settings.snake_alive_colour,
            Settings.apple_symbol: Settings.apple_colour,
        }
        if self._status == GameStatus.OVER:
            colours_map[Settings.snake_symbol] = Settings.snake_dead_colour

        for i in range(n):
            for j in range(n):
                if self.field.matrix[j][i] in what_to_draw:
                    x, y = self.__get_cell_center_coords(Point(j, i))
                    arcade.draw_rectangle_filled(
                        center_x=x,
                        center_y=y,
                        width=w,
                        height=h,
                        color=colours_map[self.field.matrix[j][i]],
                    )

    def __draw_face(self) -> None:
        """Draw snake face."""
        x, y = self.__get_cell_center_coords(self.snake.coords[-1])
        eyes_size = 2 if self._status == GameStatus.OVER else 3
        match self.snake.direction:
            case SnakeDirection.UP:
                x_shifts = (-5, 5, 0)
                y_shifts = (2, 2, 8)
            case SnakeDirection.DOWN:
                x_shifts = (-5, 5, 0)
                y_shifts = (-2, -2, -8)
            case SnakeDirection.LEFT:
                x_shifts = (-3, -3, -8)
                y_shifts = (-4, 4, 0)
            case _:
                x_shifts = (3, 3, 8)
                y_shifts = (4, -4, 0)
        # snake's eyes
        arcade.draw_rectangle_filled(
            center_x=x + x_shifts[0],
            center_y=y + y_shifts[0],
            width=eyes_size,
            height=eyes_size,
            color=Settings.snake_eyes_colour,
        )
        arcade.draw_rectangle_filled(
            center_x=x + x_shifts[1],
            center_y=y + y_shifts[1],
            width=eyes_size,
            height=eyes_size,
            color=Settings.snake_eyes_colour,
        )
        if self._status != GameStatus.OVER:
            # snake's mouth
            arcade.draw_rectangle_filled(
                center_x=x + x_shifts[2],
                center_y=y + y_shifts[2],
                width=3,
                height=3,
                color=Settings.snake_mouth_colour,
            )

    def __draw_stat(self) -> None:
        """Draw text info."""
        cell1_x = Settings.cell_size
        cell2_x = Settings.cell_size * 13
        row1_y = Settings.cell_size * (self._field_size + 3) + Settings.cell_size // 2
        row2_y = Settings.cell_size * (self._field_size + 2)

        if self._status == GameStatus.READY:
            field_info = f'Field size: {self._field_size}x{self._field_size}. Press Enter to start'
            choice_info = 'Choose field size by clicking numbers 1–5'
            arcade.draw_text(field_info, cell1_x, row1_y, Settings.text_colour)
            arcade.draw_text(choice_info, cell1_x, row2_y, Settings.text_colour)

        if self._status in {GameStatus.ACTION, GameStatus.OVER}:
            apples_info = f'Apples: {self._apples}'
            speed_info = f'Speed: {self._speed + 1} / {len(Settings.speed_list)}'
            arcade.draw_text(apples_info, cell1_x, row1_y, Settings.text_colour)
            arcade.draw_text(speed_info, cell1_x, row2_y, Settings.text_colour)

            if self._status == GameStatus.OVER:
                restart_info = 'Press Esc to restart'
                arcade.draw_text(restart_info, cell2_x, row1_y, Settings.text_colour)
