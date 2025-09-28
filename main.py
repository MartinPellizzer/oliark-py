import pygame

from mouse import *

sprite_pixel_num = 16
sprite_scale = 4
grid_size = 8

sprite_size = sprite_pixel_num * sprite_scale

pygame.init()
window = pygame.display.set_mode((800, 600))

font = pygame.font.Font(None, 48)

sprite = pygame.image.load('assets/sprites/field/test-1.png').convert_alpha()
sprite = pygame.transform.scale(sprite, (sprite_size, sprite_size))

sprite_player_1_width = 16 * sprite_scale
sprite_player_1_height = 24 * sprite_scale
sprite_player_1 = pygame.image.load('assets/sprites/player_1_front_left.png').convert_alpha()
sprite_player_1 = pygame.transform.scale(sprite_player_1, (sprite_player_1_width, sprite_player_1_height))

mouse = {
    'pos_x': 0,
    'pos_y': 0,
    'row_i': 0,
    'col_i': 0,
    'pan_executing': 0,
    'pan_mouse_start_x': 0,
    'pan_mouse_start_y': 0,
    'pan_camera_start_x': 0,
    'pan_camera_start_y': 0,
}

camera = {
    'pos_x': 100,
    'pos_y': 100,
}

def main_input():
    global running
    global sprite_scale
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                if sprite_scale < 16:
                    sprite_scale += 1
            elif event.y < 0:
                if sprite_scale > 1:
                    sprite_scale -= 1
    # mouse pos
    mouse['pos_x'], mouse['pos_y'] = pygame.mouse.get_pos()
    # mouse wheel
    if pygame.mouse.get_pressed()[1]: 
        if mouse['pan_executing'] == 0:
            mouse['pan_mouse_start_x'] = mouse['pos_x']
            mouse['pan_mouse_start_y'] = mouse['pos_y']
            mouse['pan_camera_start_x'] = camera['pos_x']
            mouse['pan_camera_start_y'] = camera['pos_y']
        mouse['pan_executing'] = 1
    else: 
        mouse['pan_executing'] = 0

def mouse_pan():
    camera['pos_x'] = mouse['pan_camera_start_x'] + (mouse['pos_x'] - mouse['pan_mouse_start_x'])
    camera['pos_y'] = mouse['pan_camera_start_y'] + (mouse['pos_y'] - mouse['pan_mouse_start_y'])
    print(camera['pos_x'], camera['pos_y'])

def main_update():
    global sprite_size
    global sprite
    sprite_size = sprite_pixel_num * sprite_scale
    sprite = pygame.transform.scale(sprite, (sprite_size, sprite_size))
    global sprite_player_1
    sprite_player_1_width = 16 * sprite_scale
    sprite_player_1_height = 24 * sprite_scale
    sprite_player_1 = pygame.transform.scale(sprite_player_1, (sprite_player_1_width, sprite_player_1_height))
    if mouse['pan_executing'] == 1:
        mouse_pan()

def main_render_debug():
    text_surface = font.render(f'''{mouse['pos_x']} - {mouse['pos_y']}''', True, '0xFF00FF00')
    window.blit(text_surface, (600, 0))
    text_surface = font.render(f'''{mouse['row_i']} - {mouse['col_i']}''', True, '0xFF00FF00')
    window.blit(text_surface, (600, 48))

def main_render():
    global window
    window.fill('#00000000')
    offset_x = sprite_size // 2
    offset_y = sprite_size // 4
    for row in range(grid_size):
        for col in range(grid_size):
            x = (col - row) * offset_x + camera['pos_x']
            y = (col + row) * offset_y + camera['pos_y']
            window.blit(sprite, (x, y))
    # render players
    window.blit(sprite_player_1, (0, 0))
    main_render_debug()
    pygame.display.flip()

running = True
while running:
    main_input()
    main_update()
    main_render()
pygame.quit()

