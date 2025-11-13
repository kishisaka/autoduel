from UnitObject import UnitObject
import math
import pygame
import MathBox


class MachineGun(UnitObject):
    def __init__(self, x, y, direction, owner):
        self.rect_height = 4
        self.width = 4
        self.height = 4
        self.owner = owner
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(surface, (56, 255, 10), (0, 0, self.width, self.height))
        hitbox = pygame.Rect(x, y, self.rect_height, self.rect_height)
        super().__init__("machine_gun", x, y, surface, hitbox, 2, 1, 1)
        self.current_speed = 10
        self.fuel = 50
        self.current_direction = direction

    def update_position(self):
        if self.fuel > 0:
            self.x = self.x + (math.sin(math.radians(self.current_direction)) * self.current_speed)
            self.y = self.y + (math.cos(math.radians(self.current_direction)) * self.current_speed)
            self.rect.x = self.x + (self.rect_height / 2)
            self.rect.y = self.y + (self.rect_height / 2)
        # fuel management
        if self.fuel <= 0:
            self.is_destroyed = True
        else:
            self.fuel = self.fuel - 1

    def isCollision(self, other_object):
        if self.rect.colliderect(other_object.rect):
            if other_object.name == "wall" or other_object.name == "enemy" or other_object.name == "player":
                self.fuel = -1
                self.is_destroyed = True
            if other_object.name == "enemy" or other_object.name == "player":
                approach = MathBox.find_approach(self.current_direction, self.name,
                                                 other_object.current_direction,
                                                 other_object.name)
                if 135 <= approach <= 224:
                    other_object.armorFront = other_object.armorFront - 10
                if 315 <= approach <= 360 or 0 <= approach <= 44:
                    other_object.armorBack = other_object.armorBack - 10
                if 45 <= approach <= 134:
                    other_object.armorRight = other_object.armorRight - 10
                if 225 <= approach <= 314:
                    other_object.armorLeft = other_object.armorLeft - 10

