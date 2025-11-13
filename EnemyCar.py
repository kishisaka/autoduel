import MathBox
from Car import Car


class EnemyCar(Car):

    def __init__(self, name, x, y, current_acceleration, armorleft, armorRight, armorFront, armorBack, armorUnder, playerCar):
        self.detectedOtherCar = False
        self.detectedWall = False
        self.shouldFire = False
        self.playerCar = playerCar
        super().__init__(name, x, y, 1, current_acceleration, 0, armorleft, armorRight, armorFront, armorBack,
                         armorUnder)

    def are_we_targeting(self):
        targetDirection = int(MathBox.get_direction_rotated(self.x, self.y, self.playerCar.x, self.playerCar.y))
        rangeToTarget = MathBox.find_range(self.x, self.y, self.playerCar.x, self.playerCar.y)
        if targetDirection == self.current_direction and rangeToTarget < 150:
            self.shouldFire = True
        else:
            self.shouldFire = False

    def isCollision(self, other_object):
        if self.rect.colliderect(other_object.rect):
            if other_object.name == "wall":
                self.detectedWall = True
            else:
                self.detectedWall = False
            super().isCollision(other_object)

    def update_direction(self, other_cars):
        # check if player car is within 200 unit radar
        rangeToTarget = MathBox.find_range(self.x, self.y, self.playerCar.x, self.playerCar.y)
        if rangeToTarget < 200:
            self.detectedOtherCar = True

        if self.detectedWall:
            # flip enemy car around so enemy does not get stuck!
            self.current_direction = (self.current_direction + 180) % 360
            if self.current_direction > 360:
                self.current_direction = 1
            self.detectedWall = False
        else:
            if self.detectedOtherCar:
                # pursuit mode on player car
                targetDirection = int(MathBox.get_direction_rotated(self.x, self.y, self.playerCar.x, self.playerCar.y))

                leftCount = 0
                currentDirection = self.current_direction
                while targetDirection != currentDirection:
                    currentDirection = currentDirection - 1
                    leftCount = leftCount + 1
                    if currentDirection < 0:
                        currentDirection = 360

                rightCount = 0
                currentDirection = self.current_direction
                while targetDirection != currentDirection:
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
                self.detectedOtherCar = False
            else:
                # no car detected, tight orbit right
                self.current_direction = self.current_direction + self.turn_mode
                if self.current_direction > 360:
                    self.current_direction = 0

    def update_acceleration(self):
        self.current_acceleration = self.current_acceleration + self.acceleration

    def update_speed(self):
        if self.current_speed < self.max_speed:
            self.current_speed = self.current_speed + self.current_acceleration
