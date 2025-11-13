
class UnitObject:
    def __init__(self, name, x, y, image, hitbox, max_speed, acceleration, current_acceleration):
        self.name = name
        self.current_speed = 0.0
        self.max_speed = max_speed
        self.acceleration = acceleration
        self.current_acceleration = current_acceleration
        self.internal_hull = 100
        self.is_accelerating = False
        self.is_decelerating = False
        self.is_turning_left = False
        self.is_turning_right = False
        self.is_firing = False
        self.x = x
        self.y = y
        self.current_direction = 0
        self.previous_direction = 0
        self.turn_mode = 2
        self.surface = image
        self.rect = hitbox
        self.fuel = -1
        self.is_destroyed = False

    def isCollision(self, other_object):
        print("do nothing")

    def update_position(self):
        print("do nothing")

    def update_direction(self, other_cars):
       print("do nothing")

    def update_acceleration(self):
        print("do nothing")

    def update_speed(self):
        print("do nothing")