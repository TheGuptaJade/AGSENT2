import pygame # Pygame impot
import geopandas as gpd # For the graph oh boy this is going to be isn't be easy to explain
from shapely.geometry import Point # This going to hard
import australialogic # this is my file for more detail go inside
import state_swinglogic # Also my file more deetail goes inside
import os # u can c what it does
import shutil # u can c what it does

# Delete deletedata.csv if it already existss
if os.path.exists("deletedata.csv"):
    os.remove("deletedata.csv")

# Copy clean_electorate_data.csv and rename the copy to deletedata.csv
shutil.copy("clean_electorate_data.csv", "deletedata.csv")

# this going to be important geopandas is like the go to python mapping for geojson which are like complex polygraphs, it is very powerfull it handle australia and all the tiny little bits of of line, very powerfull tool and very painful
gdf = gpd.read_file("australia_states.geojson")

# Explained In previous lines
pygame.init()
screen = pygame.display.set_mode((1000, 640), pygame.RESIZABLE)
pygame.display.set_caption("Australia Election 2025")
clock = pygame.time.Clock()

WHITE = (238, 238, 238) # Colours, See Readme for credits(I used open source)
BLACK = (34, 40, 49)
GRAY = (237, 233, 230)
BLUE = (0, 150, 255)

# this is where to complication begins 
minx = gdf.total_bounds[0]
miny = gdf.total_bounds[1]
maxx = gdf.total_bounds[2]
maxy = gdf.total_bounds[3]

def layout(w, h): # This is simplifier function, you could put this inside the mainloop but it just got way to annoying to adjust coordinates and hunt stuff down so 
    top = int(h * 0.15) # I wanted the screen to be dynamic so it chagnes some aspects like the text and buttons aren't but they main compontents are, 
    side = int(w * 0.25) # This is like 25% of the side goes to a side bar where a pie grapgh will live

    top_bar = pygame.Rect(0, 0, w, top) # this creates the obejct but DOES NOT DRAW IT, it take in x in the left side so 0 is the start ,y and the heigh and width 
    side_bar = pygame.Rect(w - side, top, side, h - top) 
    map_area = pygame.Rect(0, top, w - side, h - top)
    liberal_button = pygame.Rect(top_bar.x + 300, top_bar.y + 20, 160, 45) # The number I got from random testing
    labour_button = pygame.Rect(top_bar.x + 500, top_bar.y + 20, 160, 45)
    house_chart_box = pygame.Rect(side_bar.x + 10,side_bar.y + 10, side_bar.width - 20, side_bar.width - 20)
    return [top_bar, side_bar, map_area, liberal_button, labour_button, house_chart_box]

def short(name): # The GEOjson works with full names my data needs the shorted names
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

# This is where it gets complicated, you remember the gdf it renders the 
# australia map using lat and long, cause lets make everyones lives harder, so I need to convert
# into pygames system where again lets make everyone lives harder x pixels from left and y is pixels from top
# So these function convert the two one that converts into pygame and one the reverses it back into lat and long
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




# This is the main loop what you get when you hit run, it combines all the above functions and the function defined in the rpev two programs
running = True

while running:
    house_chart = australialogic.generate_house_chart(300, 300) # This is the size for the chart 
    w, h = screen.get_size() # Gets the with and highe for the scrreen at the moment so it can make the eniter thing bigger or smaller
    screen.fill(WHITE) # Makes the colour white

    top_bar, side_bar, map_area, liberal_button, labour_button, house_chart_box = layout(w, h) # This was the above function

    pygame.draw.rect(screen, BLACK, top_bar) # This actully puts the rectangles in the screen
    pygame.draw.rect(screen, GRAY, side_bar)
    house_chart = pygame.transform.scale(house_chart,(house_chart_box.width, house_chart_box.height)) # Remember in the above function I had a box, this is where the image sits that boz changes as with the screen so if the screen 
    screen.blit(house_chart, house_chart_box) # This draws the house pie grpgh inside the boz
    pygame.draw.rect(screen, (50, 100, 220), liberal_button) 
    pygame.draw.rect(screen, (220, 50, 50), labour_button)

    font = pygame.font.SysFont("Segoe UI", 28) # Creates a font for the tex
    font_label = pygame.font.SysFont("Segoe UI", 10)
    label_text = font.render("Add Swing: ", True,(255, 255, 255))
    instruction_text = font.render("Press States To Change House of Representatives ", True,(255, 255, 255)) # The true is antialias making it look less jagged
    liberal_text = font.render("+ 1% Liberal", True,(255, 255, 255)) # 
    labour_text = font.render("+1% Labour", True,(255, 255, 255)) #

    screen.blit(liberal_text, (liberal_button.x + 15, liberal_button.y)) # draws the text
    screen.blit(labour_text, (labour_button.x + 15, labour_button.y))
    screen.blit(label_text, (10, 12))
    screen.blit(instruction_text, (10, 60))
    # --- Draw map ---
    for row in gdf.itertuples(): # This give me  Pandas(Index=7, STATE_CODE='8', STATE_NAME='Australian Capital Territory', geometry=<POLYGON ((149.399 -35.319, 149.352 -35.351, 149.337 -35.34, 149.255 -35.33,...>)
        geom = row.geometry # this is just the geomeity
        if geom.geom_type == "Polygon": # This is for ACT, which is its terrotirty in NSW has it's own electorates so it a special function that toook 3 hours to figure what is going on 💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀
            polys = [geom] # A polygon is just one shape right so it doesn't is tuple of tuple of tuples, which if I iterate through it the program goes nope so I make it a list h
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
                state_swinglogic.add_swing("LP", 0.01)
                

            if labour_button.collidepoint(mouse_pos):
                old_results, new_results = state_swinglogic.add_swing("ALP", 0.01)
                print("OLD:", old_results)
                print("NEW:", new_results)
    chart = pygame.image.load("chart.png").convert_alpha()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()