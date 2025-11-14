import math
import pygame
from UnitObject import UnitObject


class Car(UnitObject):

    def __init__(self, name, x, y, max_speed, acceleration, current_acceleration, armorleft, armorRight, armorFront, armorBack, armorUnder):
        self.armorLeft = armorleft
        self.armorRight = armorRight
        self.armorFront = armorFront
        self.armorBack = armorBack
        self.armorUnder = armorUnder
        self.excessDamage = 50
        self.width = 20
        self.height = 20
        self.fire_rate = 2
        self.current_fire_rate_limiter = 1
        self.last_known_position = []
        self.selected_weapon = 0
        self.set_direction = 0
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(surface, (255, 0, 0), (0, 0, self.width, self.height))
        pygame.draw.line(surface, (0, 255, 0), (0, 18), (18, 18))
        # offset the rect position since the hitbox is smaller than the image
        hitbox = pygame.Rect(x, y, (self.height / 1), self.height / 1)
        super().__init__(name, x, y, surface, hitbox, max_speed, acceleration, current_acceleration)

    def isCollision(self, other_object):
        if self.rect.colliderect(other_object.rect):
            if other_object.name == "wall" or other_object.name == "player" or other_object.name == "enemy":
                # when hitting other object, bounce self back to the last 17th position so self can move again
                self.x = self.last_known_position[3][0]
                self.y = self.last_known_position[3][1]
                self.rect.x = self.last_known_position[3][0]
                self.rect.y = self.last_known_position[3][1]

                # stop self!
                self.current_speed = 0
                self.current_acceleration = 0
                self.is_decelerating = False
                self.is_accelerating = False

                # stop other!
                # other_object.current_speed = 0
                # other_object.current_acceleration = 0
                # other_object.is_decelerating = False
                # other_object.is_accelerating = False

    def update_position(self):
        self.last_known_position.append([self.x, self.y])
        # capture the last 20 positions so we can bounce player back when hitting walls.
        if len(self.last_known_position) > 19:
            del self.last_known_position[0]
        x_update = (math.sin(math.radians(self.current_direction)) * self.current_speed)
        y_update = (math.cos(math.radians(self.current_direction)) * self.current_speed)
        self.x = self.x + x_update
        self.y = self.y + y_update
        self.rect.x = self.x + x_update
        self.rect.y = self.y + y_update

    def update_direction(self, other_cars):
        leftCount = 0
        currentDirection = self.current_direction
        while self.set_direction != currentDirection:
            currentDirection = currentDirection - 1
            leftCount = leftCount + 1
            if currentDirection < 0:
                currentDirection = 360

        rightCount = 0
        currentDirection = self.current_direction
        while self.set_direction  != currentDirection:
            currentDirection = currentDirection + 1
            rightCount = rightCount + 1
            if currentDirection > 360:
                currentDirection = 0

        if leftCount < rightCount:
            self.current_direction = self.current_direction - self.turn_mode
            if self.current_direction < 0:
                self.current_direction = 360
        else:
            self.current_direction = self.current_direction + self.turn_mode
            if self.current_direction > 360:
                self.current_direction = 0

        # self.previous_direction = self.current_direction
        # if self.is_turning_left:
        #     self.current_direction = self.current_direction + self.turn_mode
        #     if self.current_direction > 360:
        #         self.current_direction = 0
        # if self.is_turning_right:
        #     self.current_direction = self.current_direction - self.turn_mode
        #     if self.current_direction < 0:
        #         self.current_direction = 360

    def update_acceleration(self):
        pass
        # if self.is_accelerating:
        #     self.current_acceleration = self.current_acceleration + .001
        # elif self.is_decelerating:
        #     self.current_acceleration = self.current_acceleration - .001
        # elif not self.is_accelerating and not self.is_decelerating:
        #     self.current_acceleration = 0

    def update_speed(self):
        pass
        # self.current_speed = self.current_speed + self.current_acceleration
        # # speed limits
        # if self.current_speed > self.max_speed:
        #     self.current_speed = self.max_speed
        # elif self.current_speed < -self.max_speed:
        #     self.current_speed = -self.max_speed

