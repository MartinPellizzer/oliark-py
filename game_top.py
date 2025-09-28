import pygame

pygame.init()
window = pygame.display.set_mode((800, 600))
font = pygame.font.Font(None, 48)
clock = pygame.time.Clock()

grid_size = 8

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
    'scale': 4,
}

tile = {
    'pixels': 16,
    'size': 16,
    'sprite': None,
}
tile['size'] = tile['pixels'] * camera['scale']
tile['sprite'] = pygame.image.load('assets/top/test-1.png').convert_alpha()
tile['sprite'] = pygame.transform.scale(tile['sprite'], (tile['size'], tile['size']))

player = {
    'row_i': 0,
    'col_i': 0,
    'pos_x': 0,
    'pos_y': 0,
    'pos_x_start': 0,
    'pos_y_start': 0,
    'pos_x_end': 0,
    'pos_y_end': 0,
    'sprite_width': 16,
    'sprite_height': 24,
    'sprite_1': None,
    'sprite_2': None,
    'sprite_3': None,
    'sprite_4': None,
    'sprite_5': None,
    'sprite_6': None,
    'sprite_7': None,
    'sprite_8': None,
    'sprite_cur': None,
    'sprite_cur_i': 0,
    'animation': False,
    'animation_speed': int(300 * 0.55),
    'animation_last_swap_time': 0,
    'direction_cur': 'down',
    'moving': False,
    'moving_speed': 300,
}
player['sprite_width'] = 16 * camera['scale']
player['sprite_height'] = 24 * camera['scale']
player['sprite_1'] = pygame.image.load('assets/sprites/player_1_front_left.png').convert_alpha()
player['sprite_1'] = pygame.transform.scale(player['sprite_1'], (player['sprite_width'], player['sprite_height']))
player['sprite_2'] = pygame.image.load('assets/sprites/player_1_front_right.png').convert_alpha()
player['sprite_2'] = pygame.transform.scale(player['sprite_2'], (player['sprite_width'], player['sprite_height']))
player['sprite_3'] = pygame.image.load('assets/sprites/player_1_back_left.png').convert_alpha()
player['sprite_3'] = pygame.transform.scale(player['sprite_3'], (player['sprite_width'], player['sprite_height']))
player['sprite_4'] = pygame.image.load('assets/sprites/player_1_back_right.png').convert_alpha()
player['sprite_4'] = pygame.transform.scale(player['sprite_4'], (player['sprite_width'], player['sprite_height']))
player['sprite_5'] = pygame.image.load('assets/sprites/player_1_side_left.png').convert_alpha()
player['sprite_5'] = pygame.transform.scale(player['sprite_5'], (player['sprite_width'], player['sprite_height']))
player['sprite_6'] = pygame.image.load('assets/sprites/player_1_side_right.png').convert_alpha()
player['sprite_6'] = pygame.transform.scale(player['sprite_6'], (player['sprite_width'], player['sprite_height']))
player['sprite_7'] = pygame.image.load('assets/sprites/player_1_side_left.png').convert_alpha()
player['sprite_7'] = pygame.transform.flip(player['sprite_7'], True, False)
player['sprite_7'] = pygame.transform.scale(player['sprite_7'], (player['sprite_width'], player['sprite_height']))
player['sprite_8'] = pygame.image.load('assets/sprites/player_1_side_right.png').convert_alpha()
player['sprite_8'] = pygame.transform.flip(player['sprite_8'], True, False)
player['sprite_8'] = pygame.transform.scale(player['sprite_8'], (player['sprite_width'], player['sprite_height']))
player['sprite_cur'] = player['sprite_1']
player['sprite_cur_i'] = 0

keyboard = {
    'key_arrow_up_pressed': 0,
    'key_arrow_down_pressed': 0,
    'key_arrow_left_pressed': 0,
    'key_arrow_right_pressed': 0,
}

def main_input():
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                if camera['scale'] < 16:
                    camera['scale'] += 1
            elif event.y < 0:
                if camera['scale'] > 1:
                    camera['scale'] -= 1

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        if player['moving'] == False:
            if player['col_i'] < grid_size - 1:
                player['direction_cur'] = 'right'
                print(player['direction_cur'])
                player['moving'] = True
                player['moving_start_time'] = pygame.time.get_ticks()
                player['pos_x_start'] = player_pos_x_get(player['col_i'])
                player['pos_x_end'] = player_pos_x_get(player['col_i'] + 1)
                player['pos_y_start'] = player_pos_y_get(player['row_i'])
                player['pos_y_end'] = player_pos_y_get(player['row_i'])
                player['animation'] = True
                player['sprite_cur'] = player['sprite_8']
                player['animation_last_swap_time'] = pygame.time.get_ticks()
                player['sprite_cur_i'] = 1
                player['col_i'] += 1
    if keys[pygame.K_LEFT]:
        if player['moving'] == False:
            if player['col_i'] > 0:
                player['direction_cur'] = 'left'
                print(player['direction_cur'])
                player['moving'] = True
                player['moving_start_time'] = pygame.time.get_ticks()
                player['pos_x_start'] = player_pos_x_get(player['col_i'])
                player['pos_x_end'] = player_pos_x_get(player['col_i'] - 1)
                player['pos_y_start'] = player_pos_y_get(player['row_i'])
                player['pos_y_end'] = player_pos_y_get(player['row_i'])
                player['animation'] = True
                player['sprite_cur'] = player['sprite_6']
                player['animation_last_swap_time'] = pygame.time.get_ticks()
                player['sprite_cur_i'] = 1
                player['col_i'] -= 1
    if keys[pygame.K_DOWN]:
        if player['moving'] == False:
            if player['row_i'] < grid_size - 1:
                player['direction_cur'] = 'down'
                print(player['direction_cur'])
                player['moving'] = True
                player['moving_start_time'] = pygame.time.get_ticks()
                player['pos_x_start'] = player_pos_x_get(player['col_i'])
                player['pos_x_end'] = player_pos_x_get(player['col_i'])
                player['pos_y_start'] = player_pos_y_get(player['row_i'])
                player['pos_y_end'] = player_pos_y_get(player['row_i'] + 1)
                player['animation'] = True
                player['sprite_cur'] = player['sprite_2']
                player['animation_last_swap_time'] = pygame.time.get_ticks()
                player['sprite_cur_i'] = 1
                player['row_i'] += 1
    if keys[pygame.K_UP]:
        if player['moving'] == False:
            if player['row_i'] > 0:
                print(player['direction_cur'])
                player['direction_cur'] = 'up'
                player['moving'] = True
                player['moving_start_time'] = pygame.time.get_ticks()
                player['pos_x_start'] = player_pos_x_get(player['col_i'])
                player['pos_x_end'] = player_pos_x_get(player['col_i'])
                player['pos_y_start'] = player_pos_y_get(player['row_i'])
                player['pos_y_end'] = player_pos_y_get(player['row_i'] - 1)
                player['animation'] = True
                player['sprite_cur'] = player['sprite_4']
                player['animation_last_swap_time'] = pygame.time.get_ticks()
                player['sprite_cur_i'] = 1
                player['row_i'] -= 1

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

def main_update():
    tile['size'] = tile['pixels'] * camera['scale']
    tile['sprite'] = pygame.transform.scale(tile['sprite'], (tile['size'], tile['size']))
    player['sprite_width'] = 16 * camera['scale']
    player['sprite_height'] = 24 * camera['scale']
    player['sprite_1'] = pygame.transform.scale(player['sprite_1'], (player['sprite_width'], player['sprite_height']))
    player['sprite_2'] = pygame.transform.scale(player['sprite_2'], (player['sprite_width'], player['sprite_height']))
    player['sprite_3'] = pygame.transform.scale(player['sprite_3'], (player['sprite_width'], player['sprite_height']))
    player['sprite_4'] = pygame.transform.scale(player['sprite_4'], (player['sprite_width'], player['sprite_height']))
    player['sprite_cur'] = pygame.transform.scale(player['sprite_cur'], (player['sprite_width'], player['sprite_height']))
    if mouse['pan_executing'] == 1:
        mouse_pan()
    if player['animation']:
        now = pygame.time.get_ticks()
        if now - player['animation_last_swap_time'] >= player['animation_speed']:
            if player['sprite_cur_i'] == 0: 
                if player['direction_cur'] == 'down':
                    player['sprite_cur'] = player['sprite_2']
                    player['sprite_cur_i'] = 1
                if player['direction_cur'] == 'up':
                    player['sprite_cur'] = player['sprite_4']
                    player['sprite_cur_i'] = 1
                if player['direction_cur'] == 'left':
                    player['sprite_cur'] = player['sprite_6']
                    player['sprite_cur_i'] = 1
                if player['direction_cur'] == 'right':
                    player['sprite_cur'] = player['sprite_8']
                    player['sprite_cur_i'] = 1
            else: 
                if player['direction_cur'] == 'down':
                    player['sprite_cur'] = player['sprite_1']
                    player['sprite_cur_i'] = 0
                if player['direction_cur'] == 'up':
                    player['sprite_cur'] = player['sprite_3']
                    player['sprite_cur_i'] = 0
                if player['direction_cur'] == 'left':
                    player['sprite_cur'] = player['sprite_5']
                    player['sprite_cur_i'] = 0
                if player['direction_cur'] == 'right':
                    player['sprite_cur'] = player['sprite_7']
                    player['sprite_cur_i'] = 0
            player['animation_last_swap_time'] = now
    if player['moving']:
        elapsed = pygame.time.get_ticks() - player['moving_start_time']
        t = min(elapsed / player['moving_speed'], 1.0)
        player['pos_x'] = player['pos_x_start'] + (player['pos_x_end'] - player['pos_x_start']) * t
        player['pos_y'] = player['pos_y_start'] + (player['pos_y_end'] - player['pos_y_start']) * t
        if t >= 1.0:
            player['moving'] = False
            player['animation'] = False
    clock.tick(60)

def main_render_debug():
    text_surface = font.render(f'''{mouse['pos_x']} - {mouse['pos_y']}''', True, '0xFF00FF00')
    window.blit(text_surface, (600, 0))
    text_surface = font.render(f'''{mouse['row_i']} - {mouse['col_i']}''', True, '0xFF00FF00')
    window.blit(text_surface, (600, 48))
    fps = clock.get_fps()
    text_surface = font.render(f'''FPS: {fps:.2f}''', True, '0xFF00FF00')
    window.blit(text_surface, (600, 96))

def main_render_map():
    offset_x = tile['size']
    offset_y = tile['size']
    for row in range(grid_size):
        for col in range(grid_size):
            x = col * offset_x + camera['pos_x']
            y = row * offset_y + camera['pos_y']
            window.blit(tile['sprite'], (x, y))

def player_pos_x_get(col_i):
    x = col_i * tile['size'] + camera['pos_x']
    return x

def player_pos_y_get(row_i):
    player_offset_y = int(-tile['size']*0.75)
    y = row_i * tile['size'] + camera['pos_y'] + player_offset_y
    return y

def main_render_player():
    if player['moving'] == False:
        x = player_pos_x_get(player['col_i'])
        y = player_pos_y_get(player['row_i'])
        window.blit(player['sprite_cur'], (x, y))
    else:
        player_offset_y = int(-tile['size']*0.75)
        x = player['pos_x']
        y = player['pos_y']
        window.blit(player['sprite_cur'], (x, y))

def main_render():
    window.fill('#00000000')
    main_render_map()
    main_render_player()
    main_render_debug()
    pygame.display.flip()

running = True
while running:
    main_input()
    main_update()
    main_render()
pygame.quit()

