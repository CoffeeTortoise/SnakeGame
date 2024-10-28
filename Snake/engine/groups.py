import sys
import pygame as pg
sys.path.append('engine')
from shapes import RectangleShape
from interfaces import Shape
from player import Snake


class ShapeGroup:
    """Class for grouping shapes. Has method draws and property group"""
    def __init__(self) -> None:
        self.__group: list[Shape] = []

    def draws(self, wnd: pg.Surface) -> None:
        """Draws shapes from the group list"""
        [shape.draw(wnd) for shape in self.__group]

    @property
    def group(self) -> list[Shape]:
        """Returns list of the group"""
        return self.__group


class DeathWall:
    """Border for a snake"""
    def __init__(self) -> None:
        self.__group: list[RectangleShape] = []

    def update(self, wnd: pg.Surface,
               user: Snake) -> None:
        """Draws blocks and kills a snake"""
        if len(self.__group) == 0 or not user.alive:
            return
        [shape.draw(wnd) for shape in self.__group]
        kill_head: bool = any([shape.rect.colliderect(user.head.rect) for shape in self.__group])
        if kill_head:
            user.alive = False
            return
        if len(user.tail) != 0 and any(any([tail.rect.colliderect(shape.rect) for tail in user.tail]) for shape in self.__group):
            user.alive = False

    @property
    def group(self) -> list[RectangleShape]:
        """Returns list of that group"""
        return self.__group
