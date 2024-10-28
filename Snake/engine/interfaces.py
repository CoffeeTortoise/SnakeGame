from abc import ABC, abstractmethod
import pygame as pg


# Entity interfaces

class Shape(ABC):

    @abstractmethod
    def draw(self, wnd: pg.Surface) -> None:
        """Method for blitting a shape on the screen"""
        pass

    @abstractmethod
    def resize(self, sizes: tuple[int, int]) -> None:
        """Method for resizing a shape"""
        pass

    @abstractmethod
    def change_color(self, color: tuple[int, int, int]) -> None:
        """Method for changing a color of the shape"""
        pass

    @property
    @abstractmethod
    def pos(self) -> tuple[int, int]:
        """Returns the position of a shape(left top corner)"""
        pass

    @property
    @abstractmethod
    def sizes(self) -> tuple[int, int]:
        """Returns sizes of a shape(width, height)"""
        pass


class PseudoSurface(ABC):

    @abstractmethod
    def draw(self, wnd: pg.Surface) -> None:
        """Draws that surface on another surface"""
        pass

    @property
    @abstractmethod
    def pos(self) -> tuple[int, int]:
        """Left top corner of that surface"""
        pass

    @property
    @abstractmethod
    def sizes(self) -> tuple[int, int]:
        """Width and height of that surface"""
        pass


# Group interfaces

