import pygame as pg
from typing import Any
import sys
sys.path.append('engine')
from shapes import RectangleShape
from colors import GREEN
from config import SIZE, WND_SIZE, FPS
from text import Counter


BEGIN_POS: tuple[int, int] = int(WND_SIZE[0] * .5), int(WND_SIZE[1] * .5)
SNAKE_SIZES: tuple[int, int] = SIZE, SIZE
SNAKE_SPEED: int = int(SIZE * .25)
REPEAT_CICLES: int = int(FPS * .15)


class SnakeBlock(RectangleShape):
    """Block of snake. Inherits RectangleShape class. Adds methos update_last"""
    def __init__(self,
                 pos: tuple[int, int],
                 sizes: tuple[int, int] = SNAKE_SIZES,
                 color: tuple[int, int, int] = GREEN) -> None:
        super().__init__(sizes, pos, color)
        self.last_pos: tuple[int, int] = pos
        self.pos_updated: bool = False
        self.cicle_count: int = 0

    def update_last(self) -> None:
        """Updates last position after some amount of cycles"""
        self.pos_updated = False
        if self.cicle_count >= REPEAT_CICLES:
            self.last_pos = self.rect.left, self.rect.top
            self.pos_updated = True
            self.cicle_count = 0
        self.cicle_count += 1


class Model0:
    """Basically, head of the snake (1 SnakeBlock object). Has methods: key_move, change_speed, change_axe, move_head, reflect"""
    def __init__(self,
                 speed: int = SNAKE_SPEED,
                 vertical: bool = False,
                 pos: tuple[int, int] = BEGIN_POS,
                 sizes: tuple[int, int] = SNAKE_SIZES,
                 color: tuple[int, int, int] = GREEN) -> None:
        self.head: SnakeBlock = SnakeBlock(pos, sizes, color)
        self.speed: int = speed
        self.vertical: bool = vertical

    def key_move(self) -> None:
        """Changes the direction of movement depending on keys. Methods: change_speed, change_axe, move_head"""
        codes: pg.key.ScancodeWrapper = pg.key.get_pressed()
        self.change_speed(codes)
        self.change_axe(codes)
        self.move_head()

    def change_speed(self, codes: pg.key.ScancodeWrapper) -> None:
        """Changes the speed to positive or negative depending on keycode"""
        speed: int = self.speed
        if codes[pg.K_RIGHT] or codes[pg.K_DOWN]:
            self.speed: int = Model0.reflect(speed)
        if codes[pg.K_LEFT] or codes[pg.K_UP]:
            self.speed: int = Model0.reflect(speed, positive=False)

    def change_axe(self, codes: pg.key.ScancodeWrapper) -> None:
        """Changes direction of movement to vertical or horizontal depending on keycode"""
        if codes[pg.K_RIGHT] or codes[pg.K_LEFT]:
            self.vertical = False
        if codes[pg.K_UP] or codes[pg.K_DOWN]:
            self.vertical = True

    def move_head(self) -> None:
        """Moves head of the snake depending on direction and speed"""
        if self.vertical:
            self.head.rect.move_ip(0, self.speed)
        else:
            self.head.rect.move_ip(self.speed, 0)
        self.head.update_last()

    @staticmethod
    def reflect(value: int,
                positive: bool = True) -> int:
        """Changes value to negative or positive"""
        if (value < 0) and positive:
            value *= -1
        if (value > 0) and not positive:
            value *= -1
        return value


class Model1(Model0):
    """Almost snake character. Inherits Model0 class. Adds methods: draw, update, tail_move, gain_tail, get_pos, get_x, get_y"""
    def __init__(self,
                 speed: int = SNAKE_SPEED,
                 vertical: bool = False,
                 pos: tuple[int, int] = BEGIN_POS,
                 sizes: tuple[int, int] = SNAKE_SIZES,
                 color: tuple[int, int, int] = GREEN) -> None:
        super().__init__(speed, vertical, pos, sizes, color)
        self._hungry: bool = True
        self.tail: list[SnakeBlock] = []

    def draw(self, wnd: pg.Surface) -> None:
        """Draws head and tail of the snake"""
        self.head.draw(wnd)
        if len(self.tail) == 0:
            return
        [tail.draw(wnd) for tail in self.tail]

    def update(self) -> None:
        """Updates head and parts of a tail position. Methods: key_move, tail_move"""
        self.key_move()
        self.tail_move()

    def tail_move(self) -> None:
        """Moves the tail of the snake"""
        if len(self.tail) == 0:
            return
        for i, tail in enumerate(self.tail):
            if i == 0:
                lead_tail: SnakeBlock = self.head
            else:
                lead_tail: SnakeBlock = self.tail[i - 1]
            if lead_tail.pos_updated:
                tail.pos = lead_tail.last_pos
            tail.update_last()

    def gain_tail(self) -> None:
        """Gains the tail of the snake"""
        if self._hungry:
            last_tail: SnakeBlock = self.head
            self._hungry = False
        else:
            last_tail: SnakeBlock = self.tail[-1]
        pos: tuple[int, int] = self.get_pos(last_tail)
        new_tail: SnakeBlock = SnakeBlock(pos=pos)
        self.tail.append(new_tail)

    def get_pos(self, last_tail: SnakeBlock) -> tuple[int, int]:
        """Returns position of new part of a tail"""
        if self.vertical:
            x: int = last_tail.pos[0]
            y: int = self.get_y(last_tail)
            return x, y
        else:
            y: int = last_tail.pos[1]
            x: int = self.get_x(last_tail)
            return x, y

    def get_x(self, last_tail: SnakeBlock) -> int:
        """Returns x position of new part of a tail. Uses if snake moves horizontally"""
        if self.speed > 0:
            return last_tail.pos[0] - last_tail.sizes[0]
        else:
            return last_tail.pos[0] + last_tail.sizes[0]

    def get_y(self, last_tail: SnakeBlock) -> int:
        """Returns y position of new part of a tail. Uses if snake moves vertically"""
        if self.speed > 0:
            return last_tail.pos[1] - last_tail.sizes[1]
        else:
            return last_tail.pos[1] + last_tail.sizes[1]


class Snake(Model1):
    """Snake character. 
    Adds methods: self_kill, respawn."""
    def __init__(self,
                 counter_fnt: str,
                 apples: int = 0,
                 speed: int = SNAKE_SPEED,
                 alive: bool = True,
                 vertical: bool = False,
                 pos: tuple[int, int] = BEGIN_POS,
                 sizes: tuple[int, int] = SNAKE_SIZES,
                 color: tuple[int, int, int] = GREEN) -> None:
        super().__init__(speed, vertical, pos, sizes, color)
        self.apples: int = apples
        self.alive: bool = alive
        self.counter: Counter = Counter(counter_fnt, start_value=self.apples)
        self._args: dict[str, Any] = {
                'apples': apples,
                'speed': speed,
                'alive': alive,
                'vertical': vertical,
                'pos': pos,
                'sizes': sizes,
                'color': color
                }

    def draw(self, wnd: pg.Surface) -> None:
        if self.alive:
            super().draw(wnd)
            self.counter.draw(wnd)

    def update(self) -> None:
        if self.alive:
            super().update()
            self.counter.change_value(self.apples)
            self.self_kill()

    def gain_tail(self) -> None:
        if self.alive:
            super().gain_tail()

    def self_kill(self) -> None:
        """If snake's tail has 6 or more parts, then snake can be killed due to collision with 6 or more element"""
        if len(self.tail) < 6:
            return
        if any([self.head.rect.colliderect(self.tail[i].rect) for i in range(5, len(self.tail))]):
            self.alive = False

    def respawn(self) -> None:
        """Respawns the snake. Returns it to it's original state."""
        if not self.alive:
            self._hungry = True
            self.tail.clear()
            self.apples = self._args['apples']
            self.speed = self._args['speed']
            self.alive = self._args['alive']
            self.vertical = self._args['vertical']
            self.head.pos = self._args['pos']
            self.head.resize(self._args['sizes'])
            self.head.change_color(self._args['color'])
            
