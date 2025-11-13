
from UnitObject import UnitObject
import pygame

class Wall(UnitObject):
    def __init__(self, x, y, width, height, name):
        # rect for collision detection
        hitbox = pygame.Rect(x, y, width, height)
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        # draw rec to the walls surface at 0,0
        pygame.draw.rect(surface, (255, 0, 0),  pygame.Rect(0, 0, width, height))
        super().__init__(name, x, y, surface, hitbox, 0, 0, 0)
