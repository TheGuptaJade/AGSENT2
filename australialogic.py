import pygame
import csv
import math

FILE = "deletedata.csv"
BOX_SIZE = 60
PADDING = 10

COLORS = {
    "ALP": (220, 50, 50),
    "LP": (50, 100, 220),
    "GRN": (50, 180, 80),
    "IND": (200, 200, 50),
    "Others": (150, 150, 150)
}


def load_state_data(state_code, file_name=FILE):
    electorates = []

    with open(file_name, newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            name = row["Electorate"]

            if not name.startswith(state_code + "."):
                continue

            values = {
                "ALP": float(row["ALP"]),
                "LP": float(row["LP"]),
                "GRN": float(row["GRN"]),
                "IND": float(row["IND"]),
                "Others": float(row["Others"]),
            }

            electorates.append((name, values))

    return electorates


def save_state_data(state_code, electorates, file_name=FILE):
    data = []

    with open(file_name, newline="") as f:
        x = csv.DictReader(f)
        fieldnames = x.fieldnames

        for row in x:
            data.append(row)

    for i in range(len(data)):
        row_name = data[i]["Electorate"]

        if row_name.startswith(state_code + "."):
            for seat_name, values in electorates:
                if row_name == seat_name:
                    data[i]["ALP"] = str(values["ALP"])
                    data[i]["LP"] = str(values["LP"])
                    data[i]["GRN"] = str(values["GRN"])
                    data[i]["IND"] = str(values["IND"])
                    data[i]["Others"] = str(values["Others"])

    with open(file_name, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def switch_seat(values):
    winner = max(values, key=values.get)
    value = values["ALP"]
    if winner == "GRN":
        value = values["GRN"]
        values["GRN"] = value

    elif winner == "Others":

        value = values["Others"]
        values["Others"] = value

    elif winner == "IND":
        value = values["IND"]
        values["IND"] = value

    else:
        value = values["LP"]
        values["LP"] = value

    return values





def draw_grid(screen, electorates, cols):
    boxes = []

    row = 0
    col = 0

    for name, values in electorates:
        x = PADDING + col * (BOX_SIZE + PADDING)
        y = PADDING + row * (BOX_SIZE + PADDING)

        winner = max(values, key=values.get)
        color = COLORS[winner]

        rect = pygame.Rect(x, y, BOX_SIZE, BOX_SIZE)
        pygame.draw.rect(screen, color, rect)

        boxes.append((rect, name))

        col += 1

        if col == cols:
            col = 0
            row += 1

    return boxes


def run_state_grid(state_code, file_name=FILE):
    electorates = load_state_data(state_code, file_name)

    count = len(electorates)

    cols = math.ceil(math.sqrt(count))
    rows = math.ceil(count / cols)

    width = cols * (BOX_SIZE + PADDING) + PADDING
    height = rows * (BOX_SIZE + PADDING) + PADDING

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(state_code + " Electoral Grid")

    running = True

    while running:
        screen.fill((255, 255, 255))

        grid = draw_grid(screen, electorates, cols)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                for rect, name in grid:
                    if rect.collidepoint(mouse_pos):
                        print("Clicked:", name)

                        index = int(name.split(".")[1]) - 1

                        seat_name, values = electorates[index]

                        values = switch_seat(values)

                        electorates[index] = (seat_name, values)

                        save_state_data(state_code, electorates, file_name)

                        print("Updated:", electorates[index])

        pygame.display.flip()

    return

