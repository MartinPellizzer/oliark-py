import pygame

pygame.init()
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
font = pygame.font.Font(None, 48)
clock = pygame.time.Clock()

pan_offset_x = window_width // 2
pan_offset_y = window_height // 2

level = {
    'rows_num': 99,
    'cols_num': 99,
    'tiles': [],
}

camera = {
    'pos_x': 0,
    'pos_y': 0,
    'scale': 2,
}

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
player['sprite'] = pygame.image.load('assets/sprites/player_1_front_left.png').convert_alpha()
player['sprite'] = pygame.transform.scale(player['sprite'], (player['sprite_width'], player['sprite_height']))

# level
for row_i in range(level['rows_num']):
    col = []
    for col_i in range(level['cols_num']):
        col.append(None)
    level['tiles'].append(col)

with open('level.txt') as f:
    content = f.read()
rows = content.split()
for row_i, row in enumerate(rows):
    for col_i, tile in enumerate(row.split(',')):
        if tile == 'None':
            level['tiles'][row_i][col_i] = None
        else:
            level['tiles'][row_i][col_i] = tile

tile = {
    'pixels': 16,
    'size': 16,
    'sprite': None,
}
tile['size'] = tile['pixels']
tile['sprite'] = pygame.image.load('assets/top/test-1.png').convert_alpha()
tile['sprite'] = pygame.transform.scale(tile['sprite'], (tile['size'], tile['size']))

def player_pos_x_get(col_i):
    x = col_i * tile['size']
    return x

def player_pos_y_get(row_i):
    player_offset_y = int(-tile['size']*0.75)
    y = row_i * tile['size'] + player_offset_y
    return y

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


def main_update():
    player['sprite_width'] = 16 * camera['scale']
    player['sprite_height'] = 24 * camera['scale']
    player['sprite'] = pygame.transform.scale(player['sprite'], (player['sprite_width'], player['sprite_height']))
    player['pos_x'] += 0.01
    camera['pos_x'] = player['pos_x']

def calculate_pos_x(pos_x):
    result = (pos_x - camera['pos_x']) * camera['scale'] + pan_offset_x
    # result = (pos_x * 2) - camera['pos_x'] + pan_offset_x
    return result

def calculate_pos_y(pos_y):
    result = (pos_y - camera['pos_y']) * camera['scale'] + pan_offset_y
    # result = (pos_y * 2) - camera['pos_y'] + pan_offset_y
    return result

def main_render_player():
    x = calculate_pos_x(player['pos_x'])
    y = calculate_pos_y(player['pos_y'])
    window.blit(player['sprite'], (x, y))

def main_render_player_reference(pos_x, pos_y):
    x = calculate_pos_x(pos_x)
    y = calculate_pos_y(pos_y)
    window.blit(player['sprite'], (x, y))

def main_render():
    window.fill('#00000000')
    main_render_player()
    main_render_player_reference(100, 100)
    main_render_player_reference(-50, -50)
    main_render_player_reference(-150, 75)
    pygame.display.flip()

running = True
while running:
    main_input()
    main_update()
    main_render()
pygame.quit()
