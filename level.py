import pygame

pygame.init()
window = pygame.display.set_mode((800, 600))
font = pygame.font.Font(None, 48)
clock = pygame.time.Clock()

level = {
    'rows_num': 99,
    'cols_num': 99,
    'tiles': [],
}
for row_i in range(level['rows_num']):
    col = []
    for col_i in range(level['cols_num']):
        col.append(None)
    level['tiles'].append(col)

print(level['tiles'])
level['tiles'][0][0] = 1
level['tiles'][0][1] = 1
level['tiles'][0][2] = 1
level['tiles'][0][3] = 1
level['tiles'][1][0] = 1
level['tiles'][1][1] = 1

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

def level_save():
    with open('level.txt', 'w') as f:
        for row_i in range(level['rows_num']):
            row = []
            for col_i in range(level['cols_num']):
                row.append(f'''{level['tiles'][row_i][col_i]}''')
            row = ','.join(row)
            f.write(f'{row}')
            f.write(f'\n')

def level_load():
    with open('level.txt') as f:
        content = f.read()
    rows = content.split()
    for row_i, row in enumerate(rows):
        for col_i, tile in enumerate(row.split(',')):
            if tile == 'None':
                level['tiles'][row_i][col_i] = None
            else:
                level['tiles'][row_i][col_i] = tile

def main_input():
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_s:
                level_save()
            if event.key == pygame.K_l:
                level_load()
        if event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                if camera['scale'] < 16:
                    camera['scale'] += 1
            elif event.y < 0:
                if camera['scale'] > 1:
                    camera['scale'] -= 1

    # mouse pos
    mouse['pos_x'], mouse['pos_y'] = pygame.mouse.get_pos()
    mouse['col_i'] = (mouse['pos_x'] - camera['pos_x']) // tile['size'] 
    mouse['row_i'] = (mouse['pos_y'] - camera['pos_y']) // tile['size']
    # mouse left
    if pygame.mouse.get_pressed()[0]:
        if mouse['row_i'] >= 0 and mouse['row_i'] < level['rows_num'] and mouse['col_i'] >= 0 and mouse['col_i'] < level['cols_num']:
            level['tiles'][mouse['row_i']][mouse['col_i']] = 1
    # mouse right
    if pygame.mouse.get_pressed()[2]:
        if mouse['row_i'] >= 0 and mouse['row_i'] < level['rows_num'] and mouse['col_i'] >= 0 and mouse['col_i'] < level['cols_num']:
            level['tiles'][mouse['row_i']][mouse['col_i']] = None
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
    if mouse['pan_executing'] == 1:
        mouse_pan()
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
    for row_i in range(level['rows_num']):
        for col_i in range(level['cols_num']):
            if level['tiles'][row_i][col_i] != None:
                x = col_i * offset_x + camera['pos_x']
                y = row_i * offset_y + camera['pos_y']
                window.blit(tile['sprite'], (x, y))

def main_render_grid():
    for i in range(level['cols_num']+1):
        x1 = i * tile['size'] + camera['pos_x']
        y1 = 0 + camera['pos_y']
        x2 = i * tile['size'] + camera['pos_x']
        y2 = 0 + tile['size'] * level['rows_num'] + camera['pos_y']
        pygame.draw.line(window, '0x33333300', (x1, y1), (x2, y2), 1)

    for i in range(level['rows_num']+1):
        x1 = 0 + camera['pos_x']
        y1 = i * tile['size'] + camera['pos_y']
        x2 = 0 + tile['size'] * level['cols_num'] + camera['pos_x']
        y2 = i * tile['size'] + camera['pos_y']
        pygame.draw.line(window, '0x33333300', (x1, y1), (x2, y2), 1)

def main_render():
    window.fill('#00000000')
    main_render_grid()
    main_render_map()
    main_render_debug()
    pygame.display.flip()

running = True
while running:
    main_input()
    main_update()
    main_render()
pygame.quit()


