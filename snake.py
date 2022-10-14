from basics import Point, SnakeDirection


class Snake:
    """Snake class.

    Contains all the snake's coordinates and direction of it's head
    as well as methods to operate them.
    """

    def __init__(self, coords: list[Point]) -> None:
        self._coords: list[Point] = coords
        self._direction: SnakeDirection = SnakeDirection.RIGHT

    @property
    def coords(self) -> list[Point]:
        """Get all snakes coordinates."""
        return self._coords

    @property
    def direction(self) -> SnakeDirection:
        """Get current direction."""
        return self._direction

    def redirect(self, to: SnakeDirection) -> None:
        """Set a new direction."""
        prev = self._direction
        self._direction = to
        if self.get_next_step() == self._coords[-2]:
            self._direction = prev

    def get_next_step(self) -> Point:
        """Return coordinates of next step forward."""
        head = self._coords[-1]
        match self._direction:
            case SnakeDirection.RIGHT:
                nxt = Point(head.x + 1, head.y)
            case SnakeDirection.LEFT:
                nxt = Point(head.x - 1, head.y)
            case SnakeDirection.UP:
                nxt = Point(head.x, head.y - 1)
            case _:
                nxt = Point(head.x, head.y + 1)
        return nxt

    def move_head(self, point: Point) -> None:
        """Move head to new position.

        Moving forward for snake is adding new element to the end and deleting first element,
        unless snake didn't eat apple.
        When snake eats apple, we don't cut snake's tail.
        When snake just moves forward, we cut snake's tail.
        """
        self._coords.append(point)

    def cut_tail(self) -> Point:
        """Cut the tail and return its point.

        Tail is the first element of the list.
        """
        point = self._coords[0]
        del self._coords[0]
        return point
