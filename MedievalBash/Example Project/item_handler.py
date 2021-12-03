from dataclasses import dataclass
import pygame

@dataclass
class Item:
    owned: bool
    versions: list
    index: int
    price: int
    damage: int
    location: pygame.Rect
