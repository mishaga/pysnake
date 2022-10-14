import enum
from dataclasses import dataclass


@dataclass(slots=True)
class Point:
    """Class for any point with int coordinates x and y."""

    x: int
    y: int


@enum.unique
class GameStatus(enum.Enum):
    """Enum of possible game statuses."""

    READY = enum.auto()
    ACTION = enum.auto()
    OVER = enum.auto()


@enum.unique
class SnakeDirection(enum.Enum):
    """Enum of possible snake's directions."""

    UP = enum.auto()
    DOWN = enum.auto()
    LEFT = enum.auto()
    RIGHT = enum.auto()
