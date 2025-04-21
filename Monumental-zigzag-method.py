import pygame
import sys
import itertools
import math

# Wall and brick size (mm)
WALL_WIDTH_MM = 2000
WALL_HEIGHT_MM = 2300
BRICK_WIDTH_MM = 210
BRICK_HEIGHT_MM = 50
BRICK_SPACING_HOR = 10
BRICK_SPACING_VER = 12.5
HALF_BRICK_WIDTH_MM = 110

# Section constraints
MAX_SECTION_WIDTH_MM = 800
MAX_SECTION_HEIGHT_MM = 1300

# Scale mm to pixels
SCALE = 0.2
WALL_WIDTH = int(WALL_WIDTH_MM * SCALE)
WALL_HEIGHT = int(WALL_HEIGHT_MM * SCALE)
BRICK_WIDTH = int(BRICK_WIDTH_MM * SCALE)
BRICK_HEIGHT = int(BRICK_HEIGHT_MM * SCALE)
HALF_BRICK_WIDTH = int(HALF_BRICK_WIDTH_MM * SCALE)
SPACING_HOR = int(BRICK_SPACING_HOR * SCALE)
SPACING_VER = int(BRICK_SPACING_VER * SCALE)
MAX_SECTION_WIDTH = int(MAX_SECTION_WIDTH_MM * SCALE)
MAX_SECTION_HEIGHT = int(MAX_SECTION_HEIGHT_MM * SCALE)

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((WALL_WIDTH + 40, WALL_HEIGHT + 40))
pygame.display.set_caption("Brick Wall Builder")
clock = pygame.time.Clock()

# Colors

#Background
BG_COLOR = (220, 220, 220)

#Sections
SECTION_COLORS = [
    (255, 160, 122),
    (135, 206, 250),
    (144, 238, 144),
    (255, 218, 185),
    (221, 160, 221),
    (240, 230, 140),
]

def darken_color(color, amount=60):
    return tuple(max(0, c - amount) for c in color)

# Section generator
def generate_sections():
    sections = []

    cols = math.ceil(WALL_WIDTH / MAX_SECTION_WIDTH)
    rows = math.ceil(WALL_HEIGHT / MAX_SECTION_HEIGHT)

    for row in range(rows):
        y = WALL_HEIGHT - (row + 1) * MAX_SECTION_HEIGHT
        y = max(0, y)
        h = min(MAX_SECTION_HEIGHT, WALL_HEIGHT - row * MAX_SECTION_HEIGHT)

        for col in (range(cols) if row % 2 == 0 else reversed(range(cols))):
            x = col * MAX_SECTION_WIDTH
            w = min(MAX_SECTION_WIDTH, WALL_WIDTH - col * MAX_SECTION_WIDTH)
            sections.append((x, y, w, h))

    return sections

# Brick layout builder
def build_brick_layout():
    layout = []
    color_cycle = itertools.cycle(SECTION_COLORS)
    sections = generate_sections()

    for section_color, (sx, sy, sw, sh) in zip(color_cycle, sections):
        y = sy + sh - BRICK_HEIGHT
        row = 0
        while y >= sy:
            x = sx
            row_bricks = []
            if row % 2 == 0:
                while x + BRICK_WIDTH + SPACING_HOR + HALF_BRICK_WIDTH <= sx + sw:
                    row_bricks.append((x, y, BRICK_WIDTH, section_color))
                    x += BRICK_WIDTH + SPACING_HOR
                if x + HALF_BRICK_WIDTH <= sx + sw:
                    row_bricks.append((x, y, HALF_BRICK_WIDTH, section_color))
            else:
                row_bricks.append((x, y, HALF_BRICK_WIDTH, section_color))
                x += HALF_BRICK_WIDTH + SPACING_HOR
                while x + BRICK_WIDTH <= sx + sw:
                    row_bricks.append((x, y, BRICK_WIDTH, section_color))
                    x += BRICK_WIDTH + SPACING_HOR
            if row % 2 == 1:
                row_bricks.reverse()
            layout.extend(row_bricks)
            y -= BRICK_HEIGHT + SPACING_VER
            row += 1

    return layout

# Drawing functions
def draw_brick(x, y, width, color):
    pygame.draw.rect(screen, color, (x + 20, y + 20, width, BRICK_HEIGHT))

def draw_full_preview(layout, placed_count):
    screen.fill(BG_COLOR)
    for i, (x, y, w, color) in enumerate(layout):
        draw_color = darken_color(color) if i < placed_count else color
        draw_brick(x, y, w, draw_color)
    pygame.display.flip()

# Main program
def main():
    layout = build_brick_layout()
    placed_bricks = 0
    draw_full_preview(layout, placed_bricks)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and placed_bricks < len(layout):
                    placed_bricks += 1
                    draw_full_preview(layout, placed_bricks)

        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
