import math
import os

import pygame
import sys
import time
import json

import MathBox
from Car import Car
from Wall import Wall
from MachineGun import MachineGun
from EnemyCar import EnemyCar

pygame.init()
pygame.joystick.init()

time_previous = 0
size = width, height = 600, 600
car_width, car_length = 10, 30

# debug font
font = pygame.font.Font(None, 20)

# the world
world_width, world_height = 5000, 5000
world_surface = pygame.Surface((world_width, world_height))
world_surface.fill((50, 50, 50))

bullets = []
walls = []
other_cars = []

clock = pygame.time.Clock()
running = True

screen = pygame.display.set_mode(size)

# the car and the car image
car = Car("player", 150, 150, 4, .005, 0, 100, 100, 100, 100, 100)

other_cars.append(EnemyCar("enemy", 200, 700, .005, 50, 50, 50, 50, 50, car))
other_cars.append(EnemyCar("enemy", 700, 700, .005, 50, 50, 50, 50, 50, car))
other_cars.append(EnemyCar("enemy", 700, 200, .005, 50, 50, 50, 50, 50, car))
other_cars.append(EnemyCar("enemy", 500, 500, .005, 50, 50, 50, 50, 50, car))
other_cars.append(car)

# utilities

# broken, do not use

def rotateWorld(surface):
    for wall in walls:
        loc = where_to_draw(car, wall)
        dx = int(loc[0]) - car.rect.x
        dy = int(loc[1]) - car.rect.y
        car_angle_change_rads = math.radians(90 - car.current_direction)
        rotated_dx = dx * math.cos(-car_angle_change_rads) - dy * math.sin(-car_angle_change_rads)
        rotated_dy = dy * math.cos(-car_angle_change_rads) + dy * math.cos(-car_angle_change_rads)
        screen_x = screen.get_width() // 2 + rotated_dx
        screen_y = screen.get_height() // 2 + rotated_dy
        rotated_wall = pygame.transform.rotate(wall.surface, -car_angle_change_rads)
        screen.blit(rotated_wall, (screen_x, screen_y))


def rotateImageAndBlit(original_surface, s1, angle, center_x, center_y):
    # Rotated original surface
    rotated_surf = pygame.transform.rotate(original_surface, angle)

    # Get rotated surface's rect, centered on the original point
    rotated_rect = rotated_surf.get_rect(center=(center_x, center_y))

    s1.blit(rotated_surf, rotated_rect)


def get_distance(origin, target):
    return math.hypot(target.x - origin.x, target.y - origin.y)


def get_heading(origin, target):
    return math.atan2(target.y - origin.y, target.x - origin.x)


def where_to_draw(origin, target):
    d1 = get_distance(origin, target)
    angle = get_heading(origin, target)
    x1 = (math.cos(angle) * d1) + 300
    y1 = (math.sin(angle) * d1) + 300
    return [x1,y1]


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def load_game_map():
    with open(resource_path("world_map.json")) as map_file:
        map_items = json.load(map_file)
    for map_item in map_items:
        wall_item = Wall(map_item["x"], map_item["y"], map_item["width"], map_item["height"], "wall")
        walls.append(wall_item)


load_game_map()

# Get joystick ID from command line argument, default to 2
joystick_id = 2
if len(sys.argv) > 1:
    try:
        joystick_id = int(sys.argv[1])
        print(f"Using joystick ID: {joystick_id}")
    except ValueError:
        print(f"Invalid joystick ID '{sys.argv[1]}', using default: 2")

for i in range(0, pygame.joystick.get_count()):
    print(f"Joystick {i}: {pygame.joystick.Joystick(i).get_name()}")

joystick = pygame.joystick.Joystick(joystick_id)
print(joystick.get_numaxes())
print(joystick.get_numhats())
print(joystick.get_numbuttons())
print(joystick.get_numballs())

# main game loop
while running:

    # user car controls here!
    hat_data = joystick.get_hat(0)
    x = int(joystick.get_axis(0) * 100)
    y = int(joystick.get_axis(1) * 100)
    requested_direction = int(MathBox.get_direction_rotated(0, 0, x, y))
    throttle = (MathBox.find_range(x, y, 0, 0) / 100)
    if throttle != 0:
        car.set_direction = requested_direction

    # if throttle > 0:
    #     car.is_accelerating
    # else:
    #     car.is_decelerating

    car.current_speed = throttle * car.max_speed

    print(requested_direction, throttle)

    car.is_firing = joystick.get_button(0)
    # if hat_data[0] == 1:
    #     car.is_turning_right = True
    #     car.is_turning_left = False
    # if hat_data[0] == -1:
    #     car.is_turning_left = True
    #     car.is_turning_right = False
    # if hat_data[1] == 1:
    #     car.is_accelerating = True
    #     car.is_decelerating = False
    # if hat_data[1] == -1:
    #     car.is_decelerating = True
    #     car.is_accelerating = False
    # if hat_data[0] == 0 and hat_data[1] == 0:
    #     car.is_decelerating = False
    #     car.is_accelerating = False
    #     car.is_turning_left = False
    #     car.is_turning_right = False

    time_previous = time.time() * 1000

    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()

    # center camera on car
    camera_x = car.x // 2 - 600 // 2
    camera_y = car.y // 2 - 600 // 2

    camera_rect = pygame.Rect(car.x, car.y, 600, 600)

    # draw background
    # screen.blit(world_surface, (0 +300, 0 + 300), area=pygame.Rect(camera_x, camera_y, 600, 600))

    # draw world
    for wall in walls:
        screen.blit(wall.surface, where_to_draw(car, wall))
    for other_car in other_cars:
        if other_car.name != "player":
            other_car_location = where_to_draw(car, other_car)
            rotateImageAndBlit(other_car.surface, screen, other_car.current_direction, other_car_location[0],
                               other_car_location[1])
    for bullet in bullets:
        screen.blit(bullet.surface, where_to_draw(car, bullet))
        bullet.update_position()
        if bullet.is_destroyed:
            bullets.remove(bullet)

    # draw player car in center
    rotateImageAndBlit(car.surface, screen, car.current_direction, 300, 300)

    # dump debug
    car_str = f"car_x: {int(car.x)}  car_y: {int(car.y)} car_dir: {int(car.current_direction)} " \
              f"rect: {int(car.rect.x)} {int(car.rect.y)} speed: {car.current_speed} acce: {car.acceleration}"
    text_surface = font.render(car_str, True, (255, 255, 255))
    screen.blit(text_surface, (0, 450))

    y_current = 475
    for other_car in other_cars:
        damage_str = f"damage: {other_car.name}, EX:{other_car.excessDamage}, F:{other_car.armorFront}, " \
                     f"B:{other_car.armorBack}, R:{other_car.armorLeft}, L:{other_car.armorRight} " \
                     f"u:{other_car.armorUnder} dir: {other_car.current_direction}"
        text_surface = font.render(damage_str, True, (255, 255, 255))
        screen.blit(text_surface, (0, y_current))
        y_current = y_current + 25


    # check for collisions first, then move vehicles.
    for wall in walls:
        for bullet in bullets:
            bullet.isCollision(wall)
        for other_car in other_cars:
            other_car.isCollision(wall)

    for car_a in other_cars:
        for car_b in other_cars:
            if car_a.name != car_b.name:
                car_a.isCollision(car_b)
        for bullet in bullets:
            bullet.isCollision(car_a)
            car_a.isCollision(bullet)

    for other_car in other_cars:
        other_car.update_position()
        other_car.update_direction(other_cars)
        other_car.update_acceleration()
        other_car.update_speed()
        if other_car.name == "enemy":
            other_car.are_we_targeting()
            if other_car.shouldFire:
                if other_car.current_fire_rate_limiter == other_car.fire_rate:
                    t = MathBox.get_XYOffset_given_direction_offset(other_car.current_direction, 15)
                    bullets.append(MachineGun(other_car.rect.x
                                              + t[0], other_car.rect.y + t[1], other_car.current_direction, other_car))
                    other_car.current_fire_rate_limiter = 0
                else:
                    other_car.current_fire_rate_limiter = other_car.current_fire_rate_limiter + 1

    # fire gun
    if car.is_firing:
        if car.current_fire_rate_limiter == car.fire_rate:
            # calculate initial x and y of bullet to be a bit forward of the vehicle.
            t = MathBox.get_XYOffset_given_direction_offset(car.current_direction, 15)
            bullets.append(MachineGun(car.rect.x
                                      + t[0], car.rect.y + t[1], car.current_direction, car))
            car.current_fire_rate_limiter = 0
        else:
            car.current_fire_rate_limiter = car.current_fire_rate_limiter + 1

    pygame.display.flip()
    clock.tick(60)  # limits FPS to 60