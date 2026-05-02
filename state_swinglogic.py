import csv

colours = {
    "ALP": (220, 50, 50),
    "LP": (50, 100, 220),
    "GRN": (50, 180, 80),
    "IND": (128, 0, 128),
    "Others": (150, 150, 150)
}

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

            values = {
                "ALP": float(row["ALP"]),
                "LP": float(row["LP"]),
                "GRN": float(row["GRN"]),
                "IND": float(row["IND"]),
                "Others": float(row["Others"])
            }

            electorate_winner = max(values, key=values.get)

            seat_wins[electorate_winner] += 1

    state_winner = max(seat_wins, key=seat_wins.get)

    return colours[state_winner]

def add_swing(name, amount):
    data = []

    with open("deletedata.csv", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames

        for row in reader:
            data.append(row)

    for i in range(len(data)):
        if name == "ALP":

            data[i]["ALP"] = str(float(data[i]["ALP"]) + amount)
            data[i]["LP"] = str(float(data[i]["LP"]) - amount)
        if name == "LP":
            data[i]["ALP"] = str(float(data[i]["ALP"]) + amount)
            data[i]["LP"] = str(float(data[i]["LP"]) - amount)
        data[i]["GRN"] = str(float(data[i]["GRN"]) + amount)
        data[i]["IND"] = str(float(data[i]["IND"]) + amount)
        data[i]["Others"] = str(float(data[i]["Others"]) + amount)

    with open("deletedata.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)