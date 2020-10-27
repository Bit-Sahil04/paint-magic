import pygame
import sys
import random
import math
from settings import *

try:
    from PIL import Image
except ImportError:
    print("Python Imaging Library (Pillow) not found - cannot save output")
    saving_enabled = False


class Tile:
    def __init__(self, x, y, size, pad):
        self.x = x
        self.y = y
        self.coord = (self.x, self.y)
        self.size = size - pad
        self.rect = pygame.rect.Rect(self.x, self.y, self.size, self.size)
        self.color_id = 0
        self.isDrawn = False


def light_tts(text: str, x, y, surf, size=10, color=(255, 255, 255)) -> pygame.Rect:
    font = pygame.font.SysFont('Arial', size, True)
    text_width, text_height = font.size(text)
    text = font.render(text, True, color)
    tRect = surf.blit(text, (x - (text_width / 2), y - (text_height / 2)))
    return tRect


def create_grid(surf, margin, padding, size):
    width, height = surf.get_size()
    width -= margin
    height -= margin
    rows = height // size
    cols = width // size
    gridlist = [[Tile(margin//2 + (x * size + padding), (margin // 2 + (y*size + padding)), size, padding)
                 for x in range(cols)] for y in range(rows)]

    return gridlist


def draw_grid(lines, surf):
    tempsurf = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
    tempsurf.convert_alpha()
    for line in lines:
        pygame.draw.line(tempsurf, (127, 127, 127, 68), line[0], line[1])

    return tempsurf


def lerp(v1, v2, t):
    dx = (1 - t)*v1[0] + t*v2[0]
    dy = (1 - t)*v1[1] + t*v2[1]
    return dx, dy


def cos_lerp(y1, y2, mu):
    angle = mu * math.pi
    mu2 = (1.0 - math.cos(angle)) * 0.5  # get new x-value based on cosine function
    return lerp(y1, y2, mu2)


def create_frame(surf, size):
    frame = []
    width, height = surf.get_size()
    rows = height // size
    cols = width // size

    for y in range(rows):
        frame.append([(0, y * size), (width, y * size)])
    for x in range(cols):
        frame.append([(x * size, 0), (x * size, height)])

    return frame


def get_tiles(grid, tilex, tiley, size):
    brush = []
    for i in range(-(size//2), size//2+1):
        for j in range(-(size//2), size//2+1):
            tx = tilex + j
            ty = tiley + i

            if -1 < ty < len(grid) and -1 < tx < len(grid[0]):
                brush.append(grid[ty][tx])
    return brush


def scramble(drawn):
    # global res, margin
    max_width = res[0] - margin
    max_height = res[1] - margin
    scrambled = []
    for x in range(len(drawn)):
        randx = random.randint(margin//2, max_width)
        randy = random.randint(margin//2, max_height)
        scrambled.append([(randx, randy), drawn[x].rect.center, drawn[x].color_id])

    return scrambled


def get_lerped_cells(scrambled):
    lerped = []
    # global lerp_speed, finished
    for i in scrambled:
        current = i[0]
        target = i[1]
        currentx, currenty = current
        targetx, targety = target
        if (targetx - 1 > currentx or targetx + 1 < currentx) and (targety - 1 > currenty or targety + 1 < currenty):
            dx, dy = cos_lerp(current, target, lerp_speed)
            lerped.append([(dx, dy), target, i[2]])
        else:
            dx, dy = target
            finished.append((dx, dy, i[2]))

    return lerped


def get_tilesets():
    tileset = []
    for i in range(len(colors)):
        surf = pygame.Surface((tile_size, tile_size))
        surf.fill(colors[i])
        tileset.append(surf)

    return tileset


def reset():
    global drawing_phase, scrambled_phase, scrambled_cells, finished
    drawing_phase = not drawing_phase
    scrambled_cells = scramble(drawn_cells)
    scrambled_phase = not scrambled_phase
    finished = []


pygame.init()
screen = pygame.display.set_mode(res)
FPS = 60
clock = pygame.time.Clock()
dt = 0
margin = 0
padding = 0
pygame.display.set_caption("text-magic @ Bit-Sahil04")

grid = create_grid(screen, margin, padding, tile_size)
print(len(grid), len(grid[0]), len(grid) * len(grid[0]))
lines = create_frame(screen, tile_size)
drawn_cells = []
scrambled_cells = []
finished = []
timer = 0
drawing_phase = True
scrambled_phase = False
string_images = []
frames = 0
tileset = get_tilesets()    # This is a surface the size of each tile for each color, as blitting is faster than drawing

selected_color = 0
linegrid = draw_grid(lines, screen)

while True:
    screen.fill(default_background_color)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if e.type == pygame.KEYUP:
            if e.key == pygame.K_SPACE:
                reset()
            if e.key == pygame.K_UP:
                brush_size += 1
            if e.key == pygame.K_DOWN:
                brush_size -= (1 < brush_size)

            if e.key == pygame.K_LEFT:
                selected_color = (selected_color - 1) % len(colors)
            if e.key == pygame.K_RIGHT:
                selected_color = (selected_color + 1) % len(colors)

    if display_grid:
        screen.blit(linegrid, (0, 0))

    mx, my = pygame.mouse.get_pos()
    tilex = ((mx - margin//2) // tile_size) % (len(grid[0]))
    tiley = ((my - margin//2) // tile_size) % (len(grid))
    brush_marker_size = brush_size*tile_size
    mrect = pygame.rect.Rect(mx - brush_marker_size//2, my - brush_marker_size//2, brush_marker_size, brush_marker_size)

    if scrambled_phase:
        scrambled_cells = get_lerped_cells(scrambled_cells)

        for i in range(len(scrambled_cells)):
            screen.blit(tileset[scrambled_cells[i][2]], (scrambled_cells[i][0], scrambled_cells[i][1]))

        for i in range(len(finished)):
            screen.blit(tileset[finished[i][2]], (finished[i][0], finished[i][1]))

        if silhouette:
            for tile in drawn_cells:
                tmp = tileset[tile.color_id].copy()
                tmp.set_alpha(50)
                screen.blit(tmp, tile.coord)

        if saving_enabled:
            FPS = 30
            display_stats = False
            if frames % optimization_level == 0:
                string_images.append(pygame.image.tostring(screen, "RGB"))

        if len(drawn_cells) == len(finished) and saving_enabled:
            scrambled_phase = not scrambled_phase
            output = []
            for image in string_images:
                output.append(Image.frombuffer(mode="RGB", size=res, data=image,))
            output[0].save(f'{output_name}.gif',
                           save_all=True, append_images=output[1:],
                           optimize=False, duration=duration, loop=0)
            print("done saving... exiting")
            exit(1)

    if drawing_phase:
        if pygame.mouse.get_pressed()[0]:
            tiles = get_tiles(grid, tilex, tiley, brush_size)
            for tile in tiles:
                tile.color_id = selected_color
                if tile not in drawn_cells:
                    drawn_cells.append(tile)

        if pygame.mouse.get_pressed()[2]:
            tiles = get_tiles(grid, tilex, tiley, brush_size)
            for tile in tiles:
                if tile in drawn_cells:
                    drawn_cells.remove(tile)

        for tile in drawn_cells:
            screen.blit(tileset[tile.color_id], tile.coord)

        pygame.draw.rect(screen, (255, 127, 127), mrect, 1)

    if display_stats:
        light_tts(f"{clock.get_fps():.2f} // {dt}", res[0] // 1.1, res[1] // 70, screen, size=20, color=colors[selected_color])
        light_tts(f"Pixels Drawn: {len(drawn_cells)} ", res[0] // 1.12, res[1] // 20, screen, size=20, color=colors[selected_color])
        light_tts(f"Brush size: {brush_size}", res[0] // 1.1, res[1] // 10, screen, size=20, color=colors[selected_color])
        pygame.draw.line(screen, (127, 255, 127), (0, res[1]-10), (lerp((0, res[1]-10), (res[0], res[1] - 10), len(finished)/(len(drawn_cells) + 1))), 3)

    dt = clock.tick(FPS)
    timer = pygame.time.get_ticks() // 1000
    frames += 1
    pygame.display.flip()
