import pygame
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt
import australialogic
import state_swinglogic
import os
import shutil

# Delete deletedata.csv if it already existss
if os.path.exists("deletedata.csv"):
    os.remove("deletedata.csv")

# Copy clean_electorate_data.csv and rename the copy to deletedata.csv
shutil.copy("clean_electorate_data.csv", "deletedata.csv")

# --- Data ---
gdf = gpd.read_file("australia_states.geojson")

# --- Init ---
pygame.init()
screen = pygame.display.set_mode((1000, 640), pygame.RESIZABLE)
pygame.display.set_caption("Australia Election 2025")
clock = pygame.time.Clock()

# --- Colors ---
WHITE = (238, 238, 238)
BLACK = (34, 40, 49)
GRAY = (237, 233, 230)
BLUE = (0, 150, 255)

# --- Bounds ---
minx, miny, maxx, maxy = gdf.total_bounds


def layout(w, h):
    top = int(h * 0.15)
    side = int(w * 0.25)

    top_bar = pygame.Rect(0, 0, w, top)
    side_bar = pygame.Rect(w - side, top, side, h - top)
    map_area = pygame.Rect(0, top, w - side, h - top)
    liberal_button = pygame.Rect(top_bar.x + 20, top_bar.y + 20, 160, 45)
    labour_button = pygame.Rect(top_bar.x + 200, top_bar.y + 20, 160, 45)
    return [top_bar, side_bar, map_area, liberal_button, labour_button]

def short(name):
    if name == "New South Wales":
        return "NSW"
    if name == "Victoria":
        return "VIC"
    if name == "Queensland":
        return "QLD"
    if name == "Western Australia":
        return "WA"
    if name == "South Australia":
        return "SA"
    if name == "Tasmania":
        return "TAS"
    if name == "Northern Territory":
        return "NT"
    if name == "Australian Capital Territory":
        return "ACT"


def project(x, y, area):
    return (
        area.x + (x - minx) / (maxx - minx) * area.width,
        area.y + (maxy - y) / (maxy - miny) * area.height
    )

def inverse(x, y, area):
    return (
        (x - area.x) / area.width * (maxx - minx) + minx,
        maxy - (y - area.y) / area.height * (maxy - miny)
    )


def generate_chart(values, width, height):
    values = [30, 20, 50]
    labels = ["A", "B", "C"]

    plt.figure(figsize=(width / 100, height / 100), dpi=100)
    plt.pie(values, labels=labels)
    plt.savefig("chart.png", bbox_inches="tight")
    plt.close()

chart = pygame.image.load("chart.png").convert_alpha()

# --- Loop ---
running = True

while running:
    w, h = screen.get_size()
    screen.fill(WHITE)

    top_bar, side_bar, map_area, liberal_button, labour_button = layout(w, h)

    pygame.draw.rect(screen, BLACK, top_bar)
    pygame.draw.rect(screen, GRAY, side_bar)
    pygame.draw.rect(screen, (50, 100, 220), liberal_button)
    pygame.draw.rect(screen, (220, 50, 50), labour_button)

    font = pygame.font.SysFont(None, 28)
    liberal_text = font.render("+1% Liberal", True, (255, 255, 255))
    labour_text = font.render("+1% Labour", True, (255, 255, 255))

    screen.blit(liberal_text, (liberal_button.x + 15, liberal_button.y + 12))
    screen.blit(labour_text, (labour_button.x + 15, labour_button.y + 12))

    # --- Draw map ---
    for row in gdf.itertuples():
        geom = row.geometry
        if geom is None:
            continue
        if geom.geom_type == "Polygon":
            polys = [geom]
        elif geom.geom_type == "MultiPolygon":
            polys = geom.geoms
        else:
            continue
        for poly in polys:
            points = []
            for x, y in poly.exterior.coords:
                points.append(project(x, y, map_area))
            colour = state_swinglogic.calculate_state_colour(short(row.STATE_NAME))
            pygame.draw.polygon(screen, colour, points)
            pygame.draw.polygon(screen, BLACK, points, 1)

    # --- Events ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if map_area.collidepoint(pygame.mouse.get_pos()):
                mx, my = pygame.mouse.get_pos()
                point = Point(inverse(mx, my, map_area)) # this takes the 

                for row in gdf.itertuples():
                    if row.geometry.contains(point):
                        australialogic.run_state_grid(short(row.STATE_NAME))
                        screen = pygame.display.set_mode((1000, 640), pygame.RESIZABLE)
                        pygame.display.set_caption("Australia Election 2025")
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if liberal_button.collidepoint(mouse_pos):
                state_swinglogic.add_swing("LP", 0.1)
                print('L')

            if labour_button.collidepoint(mouse_pos):
                state_swinglogic.add_swing("ALP",0.1)
                print('W')
    chart = pygame.image.load("chart.png").convert_alpha()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()