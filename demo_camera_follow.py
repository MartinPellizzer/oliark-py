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

camera = {
    'pos_x': 0,
    'pos_y': 0,
    'scale': 4,
}

sprite_pixels = 16
def entity_create():
    entity = {
        'pos_x': 0,
        'pos_y': 0,
        'pos_x_start': 0,
        'pos_y_start': 0,
        'pos_x_end': 0,
        'pos_y_end': 0,
        'col_i': 0,
        'row_i': 0,
        'size': sprite_pixels,
        'size_scaled': sprite_pixels,
        'sprite': None,
        'sprites': [],
        'direction': 'down',
        'moving': False,
        'moving_speed': 300,
        'moving_start_time': 300,
    }
    return entity

tile = entity_create()
tile['sprite'] = pygame.image.load('assets/top/test-1.png').convert_alpha()
tile['sprite'] = pygame.transform.scale(tile['sprite'], (tile['size_scaled'], tile['size_scaled']))

player = entity_create()
spritesheet = pygame.image.load('assets/sprites/cecil.png').convert_alpha()
for i in range(128//16):
    frame = spritesheet.subsurface((16 * i, 0, 16, 16))
    player['sprites'].append(frame)
player['sprite'] = player['sprites'][0]
player['sprite'] = pygame.transform.scale(player['sprite'], (player['size_scaled'], player['size_scaled']))

player_2 = entity_create()
player_2['sprite'] = pygame.image.load('assets/sprites/player_1_front_left.png').convert_alpha()
player_2['sprite'] = pygame.transform.scale(player_2['sprite'], (player_2['size_scaled'], player_2['size_scaled']))
player_2['col_i'] = 2
player_2['row_i'] = 2

def entity_turn_up():
    player['direction'] = 'up'
    player['sprite'] = player['sprites'][4]

def entity_turn_down():
    player['direction'] = 'down'
    player['sprite'] = player['sprites'][0]

def entity_turn_left():
    player['direction'] = 'left'
    player['sprite'] = player['sprites'][6]

def entity_turn_right():
    player['direction'] = 'right'
    player['sprite'] = player['sprites'][2]

def entity_move_up():
    if player['moving'] == False:
        entity_turn_up()
        if level['tiles'][player['row_i']-1][player['col_i']] != None:
            player['moving'] = True
            player['pos_x_start'] = tile['size'] * player['col_i']
            player['pos_y_start'] = tile['size'] * player['row_i']
            player['pos_x_end'] = tile['size'] * player['col_i']
            player['pos_y_end'] = tile['size'] * (player['row_i'] - 1)
            player['moving_start_time'] = pygame.time.get_ticks()
            player['row_i'] -= 1

def entity_move_down():
    if player['moving'] == False:
        entity_turn_down()
        if level['tiles'][player['row_i']+1][player['col_i']] != None:
            player['moving'] = True
            player['pos_x_start'] = tile['size'] * player['col_i']
            player['pos_y_start'] = tile['size'] * player['row_i']
            player['pos_x_end'] = tile['size'] * player['col_i']
            player['pos_y_end'] = tile['size'] * (player['row_i'] + 1)
            player['moving_start_time'] = pygame.time.get_ticks()
            player['row_i'] += 1

def entity_move_right():
    if player['moving'] == False:
        entity_turn_right()
        if level['tiles'][player['row_i']][player['col_i']+1] != None:
            player['moving'] = True
            player['pos_x_start'] = tile['size'] * player['col_i']
            player['pos_y_start'] = tile['size'] * player['row_i']
            player['pos_x_end'] = tile['size'] * (player['col_i'] + 1)
            player['pos_y_end'] = tile['size'] * player['row_i']
            player['moving_start_time'] = pygame.time.get_ticks()
            player['col_i'] += 1

def entity_move_left():
    if player['moving'] == False:
        entity_turn_left()
        if level['tiles'][player['row_i']][player['col_i']-1] != None:
            player['moving'] = True
            player['pos_x_start'] = tile['size'] * player['col_i']
            player['pos_y_start'] = tile['size'] * player['row_i']
            player['pos_x_end'] = tile['size'] * (player['col_i'] - 1)
            player['pos_y_end'] = tile['size'] * player['row_i']
            player['moving_start_time'] = pygame.time.get_ticks()
            player['col_i'] -= 1

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
        entity_move_right()
    elif keys[pygame.K_LEFT]:
        entity_move_left()
    elif keys[pygame.K_DOWN]:
        entity_move_down()
    elif keys[pygame.K_UP]:
        entity_move_up()

def main_update():
    # camera
    camera['pos_x'] = player['pos_x']
    camera['pos_y'] = player['pos_y']
    # level
    tile['size_scaled'] = tile['size'] * camera['scale']
    tile['sprite'] = pygame.transform.scale(tile['sprite'], (tile['size_scaled'], tile['size_scaled']))
    # player
    player['size_scaled'] = tile['size'] * camera['scale']
    player['sprite'] = pygame.transform.scale(player['sprite'], (player['size_scaled'], player['size_scaled']))
    # player 2
    player_2['size_scaled'] = tile['size'] * camera['scale']
    player_2['pos_x'] = player_2['col_i'] * player_2['size']
    player_2['pos_y'] = player_2['row_i'] * player_2['size']
    player_2['sprite'] = pygame.transform.scale(player_2['sprite'], (player_2['size_scaled'], player_2['size_scaled']))
    # player moving
    if player['moving']:
        elapsed = pygame.time.get_ticks() - player['moving_start_time']
        t = min(elapsed / player['moving_speed'], 1.0)
        dx = player['pos_x_end'] - player['pos_x_start']
        dy = player['pos_y_end'] - player['pos_y_start']
        player['pos_x'] = player['pos_x_start'] + dx * t
        player['pos_y'] = player['pos_y_start'] + dy * t
        if t >= 1.0:
            player['moving'] = False
            player['animation'] = False
    clock.tick(60)

def calculate_pos_x(pos_x):
    result = (pos_x - camera['pos_x']) * camera['scale'] + pan_offset_x
    return result

def calculate_pos_y(pos_y):
    result = (pos_y - camera['pos_y']) * camera['scale'] + pan_offset_y
    return result

def main_render_player():
    x = calculate_pos_x(player['pos_x'])
    y = calculate_pos_y(player['pos_y'])
    window.blit(player['sprite'], (x, y))

def main_render_player_reference(pos_x, pos_y):
    x = calculate_pos_x(pos_x)
    y = calculate_pos_y(pos_y)
    window.blit(player['sprite'], (x, y))

def main_render_map():
    for row_i in range(level['rows_num']):
        for col_i in range(level['cols_num']):
            if level['tiles'][row_i][col_i] != None:
                x = calculate_pos_x(16*col_i)
                y = calculate_pos_y(16*row_i)
                window.blit(tile['sprite'], (x, y))

def main_render_player_2():
    x = calculate_pos_x(player_2['pos_x'])
    y = calculate_pos_y(player_2['pos_y'])
    window.blit(player_2['sprite'], (x, y))

def main_render():
    window.fill('#00000000')
    main_render_map()
    main_render_player()
    main_render_player_2()
    pygame.display.flip()

running = True
while running:
    main_input()
    main_update()
    main_render()
pygame.quit()
