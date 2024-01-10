import random

from basics import Point
from settings import Settings
from snake import Snake


class Field:
    """Field class, contains matrix of coords, has link to snake and apple."""

    _matrix: list[list[int]]

    def __init__(self, field_size: int, snake: Snake) -> None:
        self._n = field_size
        self._matrix = [[0] * field_size for _ in range(field_size)]

        self.apple: Point | None = None

        # add borders to the matrix
        for i, line in enumerate(self._matrix):
            if i == 0 or i + 1 == self.n:
                for j in range(self.n):
                    line[j] = Settings.border_symbol
            else:
                line[0] = line[-1] = Settings.border_symbol

        # add snake to the matrix
        for point in snake.coords:
            self._matrix[point.x][point.y] = Settings.snake_symbol

    @property
    def n(self) -> int:
        return self._n

    @property
    def matrix(self) -> list[list[int]]:
        return self._matrix

    def add_apple(self, apple: Point) -> None:
        """Add apple to the field."""
        self.apple = apple
        self._matrix[self.apple.x][self.apple.y] = Settings.apple_symbol

    def check_next_step(self, next_step: Point) -> bool:
        """Check if it's possible to move forward."""
        if self._matrix[next_step.x][next_step.y] in (Settings.border_symbol, Settings.snake_symbol):
            return False
        return True

    def clear_cell(self, point: Point) -> None:
        """Clear cell when snake leaves it."""
        self._matrix[point.x][point.y] = 0

    def draw_snake_move(self, point: Point) -> None:
        """Fill the cell with snake symbol."""
        self._matrix[point.x][point.y] = Settings.snake_symbol

    def get_random_free_cell(self) -> Point:
        """Get random free cell.

        Free cell is one, that doesn't contain border, snake or apple.
        """
        all_free = [
            Point(i, j)
            for i in range(1, self.n)
            for j in range(1, self.n)
            if self._matrix[i][j] == 0
        ]
        return random.choice(all_free)
