import math

import pygame
import sys
import time
import json
from Car import Car
from Wall import Wall
from MachineGun import MachineGun

pygame.init()
time_previous = 0
size = width, height = 600, 600
car_width, car_length = 10, 30

# debug font
font = pygame.font.Font(None, 20)

# the world
world_width, world_height = 5000, 5000
world_surface = pygame.Surface((world_width, world_height))
world_surface.fill((50, 50, 50))

fire_rate = 30
current_fire_rate_limiter = 0

bullets = []
walls = []

clock = pygame.time.Clock()
running = True

screen = pygame.display.set_mode(size)

# the car and the car image
car = Car("player", 150, 150, 4, .001, 0)

# camera setup, center of player
camera_size= (600, 600)
camera_surface = pygame.Surface(camera_size)
camera_rect = pygame.Rect(car.rect.x + car.rect.height // 2, car.rect.x + car.rect.width // 2, camera_size[0], camera_size[1])

# utilities
def rotateImageAndBlit(original_surface, surface_to_blit_to, angle, center_x, center_y):
    # Rotated original surface
    rotated_surf = pygame.transform.rotate(original_surface, angle)

    # Get rotated surface's rect, centered on the original point
    rotated_rect = rotated_surf.get_rect(center=(center_x, center_y))

    surface_to_blit_to.blit(rotated_surf, rotated_rect)

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

def load_game_map():
    with open("world_map.json") as map_file:
        map_items = json.load(map_file)
    for map_item in map_items:
        wall_item = Wall(map_item["x"], map_item["y"], map_item["width"], map_item["height"], "wall")
        walls.append(wall_item)

load_game_map()

while running:
    time_previous = time.time() * 1000
    world_surface.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                car.is_accelerating = True
                car.is_decelerating = False
            if event.key == pygame.K_s:
                car.is_decelerating = True
                car.is_accelerating = False
            if event.key == pygame.K_a:
                car.is_turning_left = True
                car.is_turning_right = False
            if event.key == pygame.K_d:
                car.is_turning_right = True
                car.is_turning_left = False

        if event.type == pygame.KEYUP:
            car.is_accelerating = False
            car.is_decelerating = False
            car.is_turning_left = False
            car.is_turning_right = False

        if event.type == pygame.QUIT:
            sys.exit()

    # move player car
    car.update_direction()
    car.update_acceleration()
    car.update_position()
    car.update_speed()

    # move enemy cars
    for other_car in other_cars:
        other_car.update_direction()
        other_car.update_acceleration()
        other_car.update_position()
        other_car.update_speed()

    # draw grid
    for i in range(0, world_width, 100):
        for j in range(0, world_height, 100):
            pygame.draw.rect(world_surface, (0, 255, 0), (i, j, 2, 2))

    # draw world
    for wall in walls:
        world_surface.blit(wall.surface, wall.rect)
    for bullet in bullets:
        world_surface.blit(bullet.surface, bullet.rect)

    # fire fun
    if current_fire_rate_limiter == fire_rate:
        bullets.append(MachineGun(car.rect.x, car.rect.y, car.current_direction))
        current_fire_rate_limiter = 0
    else:
        current_fire_rate_limiter = current_fire_rate_limiter + 1

    # draw car
    rotateImageAndBlit(car.surface, world_surface, car.current_direction, car.rect.x, car.rect.y)

    for wall in walls:
        car.isCollision(wall)

    camera_rect.x = car.rect.x + car.rect.width // 2
    camera_rect.y = car.rect.y + car.rect.height // 2
    camera_surface.blit(world_surface, camera_rect)

    screen.fill((0,0,0))
    screen.blit(camera_surface, (0, 0))

    # dump debug
    text_str = f"car_x: {int(car.x)}  car_y: {int(car.y)} car_dir: {int(car.current_direction)} rect: {int(car.rect.x)} {int(car.rect.y)} speed: {car.current_speed} acce: {car.acceleration}"
    text_surface = font.render(text_str, True, (255, 255, 255))
    screen.blit(text_surface, (0, 500))

    pygame.display.flip()
    clock.tick(60)  # limits FPS to 60