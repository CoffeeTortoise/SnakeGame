from random import randint
import pygame as pg
import sys
sys.path.append('engine')
from config import WND_SIZE, SIZE
from colors import RED
from shapes import CircleShape
from player import Snake


RADIUS: int = int(SIZE * .5)
BOUNDS_X: tuple[int, int] = SIZE * 4, WND_SIZE[0] - SIZE * 4
BOUNDS_Y: tuple[int, int] = SIZE * 4, WND_SIZE[1] - SIZE * 4


class Apple:
    def __init__(self,
                 sound_path: str,
                 value: int = 1,
                 radius: int = RADIUS,
                 destroyed: bool = False,
                 color: tuple[int, int, int] = RED) -> None:
        x: int = randint(BOUNDS_X[0], BOUNDS_X[1])
        y: int = randint(BOUNDS_Y[0], BOUNDS_Y[1])
        center: tuple[int, int] = x, y
        self.circle: CircleShape = CircleShape(radius, center, color)
        self.sound: pg.mixer.Sound = pg.mixer.Sound(sound_path)
        self.destroyed: bool = destroyed
        self.value: int = value

    def draw(self, wnd: pg.Surface) -> None:
        if not self.destroyed:
            self.circle.draw(wnd)

    def interact(self, user: Snake) -> None:
        if self.destroyed or not user.alive:
            return
        if user.head.rect.colliderect(self.circle.rect):
            user.gain_tail()
            self.sound.play()
            user.apples += self.value
            self.destroyed = True

    def respawn(self) -> None:
        if self.destroyed:
            self.circle.pos = Apple.get_pos()
            self.destroyed = False

    @staticmethod
    def get_pos() -> tuple[int, int]:
        x: int = randint(BOUNDS_X[0], BOUNDS_X[1])
        y: int = randint(BOUNDS_Y[0], BOUNDS_Y[1])
        return x, y
