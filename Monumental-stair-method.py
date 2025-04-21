import pygame
import sys

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
pygame.display.set_caption("Stair-Step Brick Wall")
clock = pygame.time.Clock()

# Colors
BG_COLOR = (220, 220, 220) # Background color
SECTION_1_COLOR = (135, 206, 250)  # Color for Section 1 
SECTION_2_COLOR = (255, 160, 122)  # Color for Section 2 
SECTION_3_COLOR = (155, 200, 135) # Color for Section 2

def darken_color(color, amount=60):
    return tuple(max(0, c - amount) for c in color)

# Section 1
def build_section_1():
    layout = []
    
    y = WALL_HEIGHT - BRICK_HEIGHT
    pattern = [3, 2.5, 2, 1.5, 1, 0.5]  # Brick counts per row
    pattern_index = 0

    while y >= 0:
        bricks_in_row = pattern[pattern_index]
        pattern_index = (pattern_index + 1) % len(pattern)

        x = 0
        row_bricks = []

        if bricks_in_row in [2.5, 1.5]:  # Handle half-brick rows
            if x + HALF_BRICK_WIDTH <= WALL_WIDTH:
                row_bricks.append((x, y, HALF_BRICK_WIDTH, SECTION_1_COLOR))
                x += HALF_BRICK_WIDTH + SPACING_HOR
            bricks_in_row -= 0.5

        if bricks_in_row == 0.5:  # Handle the 0.5 brick row case
            if x + HALF_BRICK_WIDTH <= WALL_WIDTH:
                row_bricks.append((x, y, HALF_BRICK_WIDTH, SECTION_1_COLOR))
            layout.extend(row_bricks)
            break  # Stop after placing the 0.5 row

        # Place full bricks for this row
        for _ in range(int(bricks_in_row)):
            if x + BRICK_WIDTH <= WALL_WIDTH:
                row_bricks.append((x, y, BRICK_WIDTH, SECTION_1_COLOR))
                x += BRICK_WIDTH + SPACING_HOR

        layout.extend(row_bricks)
        y -= BRICK_HEIGHT + SPACING_VER

    return layout

# Section 2
def build_section_2():
    layout = []
    
    # Base starting x position: where Section 1 ends
    base_x = (BRICK_WIDTH + SPACING_HOR) * 3
    
    y = WALL_HEIGHT - BRICK_HEIGHT
    rows_to_build = 6  # Up to 6 rows
    
    for row in range(rows_to_build):
        # Apply half-brick shift per row
        x = base_x - (row * HALF_BRICK_WIDTH)

        # Fix horizontal spacing for odd rows
        if row % 2 == 1:
            x += SPACING_HOR

        row_bricks = []

        # Place 1 full brick, as this is within building envelope
        for _ in range(1):
            if x + BRICK_WIDTH <= WALL_WIDTH + MAX_SECTION_WIDTH:
                row_bricks.append((x, y, BRICK_WIDTH, SECTION_2_COLOR))
                x += BRICK_WIDTH + SPACING_HOR

        layout.extend(row_bricks)
        y -= BRICK_HEIGHT + SPACING_VER

    return layout

# Section 3
def build_section_3():
    layout = []
    
    # Base starting x position: where Section 1 ends
    base_x = (BRICK_WIDTH + SPACING_HOR) * 4
    
    y = WALL_HEIGHT - BRICK_HEIGHT
    rows_to_build = 6  # Up to 6 rows, because this is max within build envelope
    
    for row in range(rows_to_build):
        # Apply half-brick shift per row
        x = base_x - (row * HALF_BRICK_WIDTH)

        # Fix horizontal spacing for odd rows
        if row % 2 == 1:
            x += SPACING_HOR

        row_bricks = []

        # Place 1 full brick, as this is within building envelope
        for _ in range(1):
            if x + BRICK_WIDTH <= WALL_WIDTH + MAX_SECTION_WIDTH:
                row_bricks.append((x, y, BRICK_WIDTH, SECTION_3_COLOR))
                x += BRICK_WIDTH + SPACING_HOR

        layout.extend(row_bricks)
        y -= BRICK_HEIGHT + SPACING_VER

    return layout

# Drawing functions
def draw_brick(x, y, width, color):
    pygame.draw.rect(screen, color, (x + 20, y + 20, width, BRICK_HEIGHT))

def draw_full_preview(layout, placed_count):
    screen.fill(BG_COLOR)

    # Draw the layout with both sections
    for i, (x, y, w, color) in enumerate(layout):
        draw_color = darken_color(color) if i < placed_count else color
        draw_brick(x, y, w, draw_color)
    
    pygame.display.flip()

# Main program
def main():
    # Build Section 1 and Section 2
    section_1_layout = build_section_1()
    section_2_layout = build_section_2()
    section_3_layout = build_section_3()
    
    # Combine layouts
    layout = section_1_layout + section_2_layout + section_3_layout
    
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
