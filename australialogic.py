import pygame # Basic Imports
import csv # Basic Imports
import math # Basic Imports
import matplotlib.pyplot as plt # Basic Imports


BOX_SIZE = 60 # For the boxes
PADDING = 10 # For the boxes

COLOURS = { # Just colours
    "ALP": (220, 50, 50),
    "LP": (50, 100, 220),
    "GRN": (50, 180, 80),
    "IND": (128, 0, 128),
    "Others": (150, 150, 150)
}

COLOURS_FOR_PIE = { # For some very weird reason matpolt doesn't like RGB, needs to special values between 0 and 1
    "ALP": (220 / 255, 50 / 255, 50 / 255),
    "LP": (50 / 255, 100 / 255, 220 / 255),
    "GRN": (50 / 255, 180 / 255, 80 / 255),
    "IND": (128 / 255, 0 / 255, 128 / 255),
    "Others": (150 / 255, 150 / 255, 150 / 255)
}

def get_current_winner(row): # gets the winner
    return row['Winner']


def load_all_electorates(): # this function was created to simplify the code, I could just put this inside the generate_pie but it just gets way to complicted
    electorates = [] # This is a list

    with open("deletedata.csv") as f: # This is in python a way to use read files, it can't write cause it doesn't have the permisions
        reader = csv.DictReader(f)
        for row in reader: # iterates through row
            electorates.append(row) # Puts the row in reader

    return electorates 

def generate_house_chart(width, height): # A function for creating the pie chart
    electorates = load_all_electorates() # Calls the function above

    party_counts = { "ALP": 0,"LP": 0,"GRN": 0,"IND": 0,"Others": 0} # This is a list of the main parties, in australia everthing else goes into others

    for row in electorates: # The output would look something like [{'ALP', 'WinnerShare': '0.6328322429206412', 'RunnerUpShare': '0.3671677570793587', 'Margin': '0.2656644858412825'}] and when you iterate through it get the dictionary
        winner = row["Winner"] # This finds the winner

        if winner not in party_counts: # if it some weird party like KAP then it goes into others
            winner = "Others"

        party_counts[winner] += 1 # adds one to each of the winners so if ALP had 4 winners then another pops up it becomes 5

    labels = [] # Would u look at another list
    sizes = [] # You guessed it is a list
    colours = [] #  Yipee a list 

    for party in party_counts.keys(): # iterates through each key, in python  dictionary is split up into two parts, a key and a value in this case the key is the party name
            labels.append(party) # this adds it to the labels list
            sizes.append(party_counts[party]) # adds to the size
            colours.append(COLOURS_FOR_PIE[party]) # the colours for pie see above explained added to colours list

    total_seats = sum(sizes) # needed for calculations of percentages

    def show_seats(percent): # needed for the pie chart, but not in the way you thin
        seats = round(percent * total_seats / 100) # this is the reversal of a percentage, important
        return str(seats)# makes it a string

    plt.figure(figsize=(width / 100, height / 100), dpi=100) # This where USA make no sense it generates the pie chart inches the reason I divided eveything by 100 is becuase I set the DPI 100 pixels/dots per inch. This is important becuase pygmes hates anything but pixels so I need convert to pixels to inches and cause I set DPI to 100 just divide everthyn by 100
    plt.pie(sizes, labels=labels, colors=colours, autopct=show_seats) # feels self explanitory here but the autopct is a little weird it controls the text inside the pie graph remeber the function earlier what does is reverses the already converted percentage of seats into the actual seat number, without it students would see the percentage of seats
    plt.title("House of Representatives Seats") # A title
    plt.savefig("chart.png", bbox_inches="tight") # the bbox removes the extra space 
    plt.close() # this closes the file and puts in the folder

    chart = pygame.image.load("chart.png").convert_alpha() # This converts into a pygame ready loadable so u just need to input this with the cordintes and it should come up the convert alpha makes it transparent

    return chart # Returns chart

def load_state_data(state_code): # This for state data will explain later
    electorates = [] # a list.

    with open("deletedata.csv") as f: # as seen above
        reader = csv.DictReader(f) # this is interable object 

        for row in reader: # iterates though it 
            name = row["Electorate"] # gets the NSW.1

            if name.startswith(state_code + "."): # This where my naming system came ie NSW.1, big brain move, but for know .startswith is a string that returns true if the conditions are met
                electorates.append(row) # Adds to row

    return electorates # gives it bakc

def save_state_data(electorates): # This is important, it saves the information,
    data = [] # This is the old data list
    fieldnames = []# another list
    with open("deletedata.csv") as f: # seen this a bunch of times
        reader = csv.DictReader(f) 
        fieldnames = reader.fieldnames # this creates a list of field names, kinda like this ["Electorate", "StateAb", "DivisionID", "DivisionNm", "Winner", "RunnerUp", "WinnerShare", "RunnerUpShare", "Margin"]

        for row in reader:
            data.append(row)

    for i in range(len(data)): # iterates through the data
        row_name = data[i]["Electorate"] # This finds the name of the row

        for changed_row in electorates: # Iterates through each new data very inneficient yes, but accurate
            if row_name == changed_row["Electorate"]: # Gets the right row
                data[i] = changed_row # replaces the row

    with open("deletedata.csv", "w",) as f: # The w is new, it just allows for replacing and writing new
        writer = csv.DictWriter(f, fieldnames=fieldnames) # Cause we work with dictionaries I can't just use  a normal CSV writer but a writer for dictionaries
        writer.writeheader() # This writes the headers, a list of headers(this is above)
        writer.writerows(data) # iterates through the data list, oh and if you are actually reading these comments I  
# If you read through all my comments you might be confused, the reason I had  a data list was becuase it had to hold all the data not jsut fro mteh state
def switch_seat(row): # This is for switiching the seats
    old_winner = row["Winner"] # The old winnder
    old_runner_up = row["RunnerUp"] # The new winner

    row["Winner"] = old_runner_up # This replaces the data
    row["RunnerUp"] = old_winner 

    old_winner_share = row["WinnerShare"] # Switches by how much they won by
    old_runner_up_share = row["RunnerUpShare"]

    row["WinnerShare"] = old_runner_up_share
    row["RunnerUpShare"] = old_winner_share

    row["Margin"] = str(float(row["WinnerShare"]) - float(row["RunnerUpShare"])) # new marign

    return row # returns the row

def draw_grid(screen, electorates, cols): # This draws the grid
    boxes = [] # a list for the objects that will be the bobex

    row_number = 0 # The number of rows the screen will have
    col_number = 0 # The amount of colunms 

    for row in electorates: # iterates through the colunms
        x = PADDING + col_number * (BOX_SIZE + PADDING)  # This calculates the x position the col_number + padding * the actual size of the box
        y = PADDING + row_number * (BOX_SIZE + PADDING)

        winner = get_current_winner(row) # gets the winner
        colour = COLOURS[winner] # finds winner colour

        rect = pygame.Rect(x, y, BOX_SIZE, BOX_SIZE) # this places a rectanangel
        pygame.draw.rect(screen, colour, rect) # this actuall places the rectanlge

        boxes.append((rect, row)) # this adds the object plus the row(for finidng if it pressed)

        col_number += 1 # adds one to colunms

        if col_number == cols: # if the max colunm is reache move down a row
            col_number = 0
            row_number += 1

    return boxes

def run_state_grid(state_code):
    electorates = load_state_data(state_code)

    count = len(electorates)

    cols = math.ceil(math.sqrt(count)) # Finds the whole number of the amount of colunms by finding the quire root for instand if you have 46 electorates(NSW)  you need a 7x7 gird so you have space for 49 electorates when u square root 6.78 round up and you get 7
    rows = math.ceil(count / cols) # Finds the row amount for the nsw exapml 46/7 = 6.75 = 7 rows

    width = cols * (BOX_SIZE + PADDING) + 2*PADDING # finds the heigt, the padding is multiplied by two cause two side
    height = rows * (BOX_SIZE + PADDING) + 2*PADDING

    pygame.init() # Initiies pygme
    screen = pygame.display.set_mode((width, height)) # sets the displat
    pygame.display.set_caption(state_code + " Electoral Grid") # And caption

    running = True # will see later

    while running:
        screen.fill((255, 255, 255)) # this is black

        grid = draw_grid(screen, electorates, cols) # this draws the grid

        for event in pygame.event.get(): # checks if the x button is pressed and kills the game
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN: # checks for a clikc
                mouse_pos = pygame.mouse.get_pos() # gets the x, and y positio

                for rect, row in grid: # iterates through each electorate grid
                    if rect.collidepoint(mouse_pos): # This is a godsend, it checks for if the mouse points where in the boxes 
                        print("Clicked:", row["Electorate"], row["DivisionNm"]) # This is a debugging check 

                        changed_row = switch_seat(row) # Switches the seat

                        for i in range(len(electorates)): # This goes through electorate in the stae
                            if electorates[i]["Electorate"] == changed_row["Electorate"]: # if the changed row matches with the eltorate data
                                electorates[i] = changed_row # update

                        save_state_data(electorates) # pushes to a temp file

                        print("New winner:", changed_row["Winner"]) # More debuging

        pygame.display.flip() # Keeps the screen running

    