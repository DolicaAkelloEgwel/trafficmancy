import csv

import tflwrapper

# Get the app key for API requests
with open("./app.key", "r") as f:
    APP_KEY = f.readline()

# Station Name
STRATFORD = "Stratford"

# Line Names
CENTRAL = "central"
ELIZABETH = "elizabeth"
MILDMAY = "mildmay"
JUBILEE = "jubilee"
DLR = "dlr"

# ID of the bike point near Stratford Station
STRATFORD_BIKE_POINT_ID = "BikePoints_790"

# API has some confusing thing where "elizabeth" is used in some places and "elizabeth-line" is used in others but "dlr" is consistent...
STRATFORD_LINES = ["elizabeth-line", DLR, "tube"]

# List of the lines that pass through Stratford station
LINES_THAT_GO_THROUGH_STRATFORD = [ELIZABETH, DLR, CENTRAL, MILDMAY, JUBILEE]

# Get the different Naptans for Stratford station
STRATFORD_NAPTANS = {line_name: None for line_name in LINES_THAT_GO_THROUGH_STRATFORD}

# Dictionary for the termini Naptans for all the different lines that pass through Stratford
TERMINI_NAPTANS = {line_name: [] for line_name in LINES_THAT_GO_THROUGH_STRATFORD}

with open("./data/stratford-naptans.csv", "r") as csvfile:
    naptan_file = csv.reader(csvfile)
    for line_name, naptan in naptan_file:
        STRATFORD_NAPTANS[line_name] = naptan

with open("./data/terminus-naptans.csv", "r") as csvfile:
    naptan_file = csv.reader(csvfile)
    for row in naptan_file:
        TERMINI_NAPTANS[row[0]] = row[1:]

# Find info on trains heading to/from Stratford
line = tflwrapper.line(APP_KEY)

for line_name in TERMINI_NAPTANS:
    for terminus_naptan in TERMINI_NAPTANS[line_name]:
        arrivals = line.getArrivalsByNaptan(
            [line_name], STRATFORD_NAPTANS[line_name], terminus_naptan
        )


def get_tfl_data():
    data = {}

    # Get number of broken lifts across TFL network
    disruptions = tflwrapper.disruptions(APP_KEY)
    data["num-broken-lifts"] = len(disruptions.getAllLifts())

    # Get today's air quality data
    air_quality = tflwrapper.airQuality(APP_KEY)
    data["air-quality"] = air_quality.getAirQuality()["currentForecast"][0][
        "forecastSummary"
    ]

    # Find status of the different lines that pass through Stratford
    line = tflwrapper.line(APP_KEY)
    statuses = line.getStatusByID(STRATFORD_LINES, True)
    status_info = ""
    for status in statuses:
        if status["id"] in LINES_THAT_GO_THROUGH_STRATFORD:
            status_info += f" {status['name']} has {len(status['disruptions'])} disruptions and has {status['lineStatuses'][0]['statusSeverityDescription']}."

    data["statford-line-data"] = status_info[1:]

    return data


print(get_tfl_data())
