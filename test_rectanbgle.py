import pygame
import math

# Init
pygame.init()
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
pygame.display.set_caption("Centered Rotation")

# Colors
RED = (255, 0, 0)
BG = (30, 30, 30)

# Rectangle size
rect_width, rect_height = 30, 10

# Create original surface with alpha support
original_surf = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA)
pygame.draw.rect(original_surf, RED, (0, 0, rect_width, rect_height))

# Define center of rotation (screen center)
center_x, center_y = 400, 400

angle = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    angle += 1

    # Rotate original surface
    rotated_surf = pygame.transform.rotate(original_surf, angle)

    # Get rotated surface's rect, centered on the original point
    rotated_rect = rotated_surf.get_rect(center=(0, 0))

    # Rotate original surface
    rotated_surf2 = pygame.transform.rotate(original_surf, angle)

    # Get rotated surface's rect, centered on the original point
    rotated_rect2 = rotated_surf2.get_rect(center=(50, 50))

    # Draw everything
    screen.fill(BG)
    screen.blit(rotated_surf, rotated_rect)
    screen.blit(rotated_surf2, rotated_rect2)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()