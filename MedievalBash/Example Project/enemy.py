import pygame
from dataclasses import dataclass


@dataclass
class Enemy:
    x_change: int
    y_change: int
    sprite: pygame.surface
    rect: pygame.rect
    speed: int
    index: int

