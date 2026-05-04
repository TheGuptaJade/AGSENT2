import csv # Imports

colours = { # The colours
    "ALP": (220, 50, 50),
    "LP": (50, 100, 220),
    "GRN": (50, 180, 80),
    "IND": (128, 0, 128),
    "Others": (150, 150, 150)
}

def fix_party_name(party): # Nomilises the party so if it isn't the colours it goes into other sections
    if party in colours:
        return party
    else:
        return "Others"


def get_current_winner(row): # gets the winner
    return row['Winner'] # Returns the winner
def calculate_state_colour(state): # finds the state colour
    seat_wins = { "ALP": 0, "LP": 0, "GRN": 0, "IND": 0, "Others": 0} # Finds the seat wins
    with open("deletedata.csv") as f: # Opens the data
        reader = csv.DictReader(f) # The reader an object

        for row in reader: # I explained this in australialogic
            electorate = row["Electorate"]

            if not electorate.startswith(state + "."):
                continue

            winner = fix_party_name(row["Winner"])
            seat_wins[winner] += 1

    state_winner = max(seat_wins, key=seat_wins.get) # Finds the max, know this is new for me so the seat_wins.get that is actually the fucntion so what this is iteraptes through each entry and gets the value(.get) for each and then finds the max, I suspect it uses a liner search algorim, ask me if you have question I am not typing up how that works

    return colours[state_winner] # Gives the colour

def count_party_seats():
    seat_wins = {
        "ALP": 0,
        "LP": 0,
        "GRN": 0,
        "IND": 0,
        "Others": 0
    }

    with open("deletedata.csv", newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            winner = fix_party_name(row["Winner"])
            seat_wins[winner] += 1

    return seat_wins

def add_swing(name, amount):
    data = []

    old_seat_wins = count_party_seats() # Counts how many seats each party has before the swing is applied

    with open("deletedata.csv") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames # Needed for placing data back

        for row in reader: # Iterates through every single dataset
            winner = row["Winner"] # Current Winning Pary
            runner_up = row["RunnerUp"] # Current Second Place

            winner_share = float(row["WinnerShare"]) # How Much did Winning win 
            runner_up_share = float(row["RunnerUpShare"]) # How much did runner up have

            if name == winner: # Name = winner
                winner_share += amount # Increases the amount the winner by
                runner_up_share -= amount # Increases the amount the runner up lost by

            elif name == runner_up:
                winner_share -= amount # Reduces the winner
                runner_up_share += amount # increases the loser

            if winner_share < 0: # Sometimes the winners goes into negative tht isn't posible so this removies it
                winner_share = 0

            if runner_up_share < 0: # Same for the runner
                runner_up_share = 0

            if winner_share > 1: # since 1 is 100% anything higher be wrong
                winner_share = 1

            if runner_up_share > 1: # Same for the runner up
                runner_up_share = 1


            row["Winner"] = winner
            row["RunnerUp"] = runner_up
            row["WinnerShare"] = str(winner_share)
            row["RunnerUpShare"] = str(runner_up_share)
            row["Margin"] = str(winner_share - runner_up_share)

            data.append(row)

    with open("deletedata.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    new_seat_wins = count_party_seats()

    return old_seat_wins, new_seat_wins # For degibbung print states