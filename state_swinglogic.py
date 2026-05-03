import csv

colours = {
    "ALP": (220, 50, 50),
    "LP": (50, 100, 220),
    "GRN": (50, 180, 80),
    "IND": (128, 0, 128),
    "Others": (150, 150, 150)
}

def fix_party_name(party):
    if party in colours:
        return party
    else:
        return "Others"


def get_current_winner(row):
    return row['Winner']
def calculate_state_colour(state):
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
            electorate = row["Electorate"]

            if not electorate.startswith(state + "."):
                continue

            winner = fix_party_name(row["Winner"])
            seat_wins[winner] += 1

    state_winner = max(seat_wins, key=seat_wins.get)

    return colours[state_winner]

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

    old_seat_wins = count_party_seats()

    with open("deletedata.csv", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames

        for row in reader:
            winner = row["Winner"]
            runner_up = row["RunnerUp"]

            winner_share = float(row["WinnerShare"])
            runner_up_share = float(row["RunnerUpShare"])

            if name == winner:
                winner_share += amount
                runner_up_share -= amount

            elif name == runner_up:
                winner_share -= amount
                runner_up_share += amount

            if winner_share < 0:
                winner_share = 0

            if runner_up_share < 0:
                runner_up_share = 0

            if winner_share > 1:
                winner_share = 1

            if runner_up_share > 1:
                runner_up_share = 1

            total = winner_share + runner_up_share

            if total != 0:
                winner_share = winner_share / total
                runner_up_share = runner_up_share / total

            if runner_up_share > winner_share:
                temp_party = winner
                winner = runner_up
                runner_up = temp_party

                temp_share = winner_share
                winner_share = runner_up_share
                runner_up_share = temp_share

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

    return old_seat_wins, new_seat_wins