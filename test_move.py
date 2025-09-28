import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

x = 100
speed = 5

while True:
    clock.tick(60)  # Ensure consistent 60 FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:
        x += speed
    if keys[pygame.K_LEFT]:
        x -= speed

    screen.fill((30, 30, 30))
    pygame.draw.rect(screen, (255, 0, 0), (x, 250, 50, 50))
    pygame.display.flip()
