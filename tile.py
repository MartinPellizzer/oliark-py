import pygame

pygame.init()
window = pygame.display.set_mode((800, 600))

image_size = 16
image_scale = 2
cell_size = image_size * image_scale

pen_color = '#FFFFFFFF'

# init pixel matrix
pixel_matrix = []
for i in range(image_size):
    row = []
    for j in range(image_size):
        row.append('#00000000')
    pixel_matrix.append(row)

# pixel_matrix[0][0] = '#FF0000FF'
# pixel_matrix[0][1] = '#00FF00FF'
# pixel_matrix[1][0] = '#0000FFFF'

def image_save():
    surface = pygame.Surface((image_size, image_size), pygame.SRCALPHA, 32)
    for y in range(image_size):
        for x in range(image_size):
            surface.set_at((x, y), pixel_matrix[y][x])
    pygame.image.save(surface, 'test-1.png')

def image_load():
    global pixel_matrix
    pixel_matrix = []
    image = pygame.image.load('test-1.png').convert_alpha()
    for y in range(image_size):
        row = []
        for x in range(image_size):
            rgba = image.get_at((x, y))
            r, g, b, a = rgba
            pixel_hex = f'#{r:02X}{g:02X}{b:02X}{a:02X}'
            row.append(pixel_hex)
        pixel_matrix.append(row)    


# quit()

print(pixel_matrix)

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
    global pixel_matrix
    global image_scale
    global pen_color
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_1:
                pen_color = '#FFFFFFFF'
            if event.key == pygame.K_2:
                pen_color = '#888888FF'
            if event.key == pygame.K_c:
                pixel_matrix = []
                for i in range(image_size):
                    row = []
                    for j in range(image_size):
                        row.append('#00000000')
                    pixel_matrix.append(row)
            if event.key == pygame.K_s:
                image_save()
            if event.key == pygame.K_l:
                image_load()
        if event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                if image_scale < 8:
                    image_scale += 1
            elif event.y < 0:
                if image_scale > 1:
                    image_scale -= 1
    mouse_buttons = pygame.mouse.get_pressed()
    # mouse left
    if mouse_buttons[0]:
        if mouse['row_i'] >= 0 and mouse['row_i'] < image_size and mouse['col_i'] >= 0 and mouse['col_i'] < image_size:
            pixel_matrix[mouse['row_i']][mouse['col_i']] = pen_color
    # mouse right
    if mouse_buttons[2]:
        if mouse['row_i'] >= 0 and mouse['row_i'] < image_size and mouse['col_i'] >= 0 and mouse['col_i'] < image_size:
            pixel_matrix[mouse['row_i']][mouse['col_i']] = '#00000000'
    # mouse wheel
    if mouse_buttons[1]: 
        if mouse['pan_executing'] == 0:
            mouse['pan_mouse_start_x'] = mouse['pos_x']
            mouse['pan_mouse_start_y'] = mouse['pos_y']
            mouse['pan_camera_start_x'] = camera['pos_x']
            mouse['pan_camera_start_y'] = camera['pos_y']
        mouse['pan_executing'] = 1
    else: 
        mouse['pan_executing'] = 0
    mouse['pos_x'], mouse['pos_y'] = pygame.mouse.get_pos()
    mouse['col_i'] = (mouse['pos_x'] - camera['pos_x']) // cell_size 
    mouse['row_i'] = (mouse['pos_y'] - camera['pos_y']) // cell_size

def mouse_pan():
    camera['pos_x'] = mouse['pan_camera_start_x'] + (mouse['pos_x'] - mouse['pan_mouse_start_x'])
    camera['pos_y'] = mouse['pan_camera_start_y'] + (mouse['pos_y'] - mouse['pan_mouse_start_y'])
    pass

def main_update():
    global cell_size
    cell_size = image_size * image_scale
    if mouse['pan_executing'] == 1:
        mouse_pan()

def main_draw_grid():
    for i in range(image_size+1):
        x1 = i * cell_size + camera['pos_x']
        y1 = 0 + camera['pos_y']
        x2 = i * cell_size + camera['pos_x']
        y2 = 0 + cell_size * image_size + camera['pos_y']
        pygame.draw.line(window, '0x33333300', (x1, y1), (x2, y2), 1)

        x1 = 0 + camera['pos_x']
        y1 = i * cell_size + camera['pos_y']
        x2 = 0 + cell_size * image_size + camera['pos_x']
        y2 = i * cell_size + camera['pos_y']
        pygame.draw.line(window, '0x33333300', (x1, y1), (x2, y2), 1)

def main_draw_pixel_matrix():
    for row_i in range(image_size):
        for col_i in range(image_size):
            pixel = pixel_matrix[row_i][col_i]
            if pixel != '#00000000':
                x = col_i * cell_size + camera['pos_x']
                y = row_i * cell_size + camera['pos_y']
                w = cell_size
                h = cell_size
                pygame.draw.rect(window, pixel, (x, y, w, h))

def main_render():
    window.fill('#111111')
    main_draw_grid()
    main_draw_pixel_matrix()
    # debug
    text_surface = font.render(f'''{mouse['pos_x']} - {mouse['pos_y']}''', True, '0xFF00FF00')
    window.blit(text_surface, (600, 0))
    text_surface = font.render(f'''{mouse['row_i']} - {mouse['col_i']}''', True, '0xFF00FF00')
    window.blit(text_surface, (600, 48))
    pygame.display.flip()

font = pygame.font.Font(None, 48)
running = True
while running:
    main_input()
    main_update()
    main_render()
pygame.quit()

