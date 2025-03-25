import csv

import tflwrapper

# Get the app key for API requests
with open("./app.key", "r") as f:
    APP_KEY = f.readline()

# ID for road around Stratford
A12 = "a12"

# API has some confusing thing where "elizabeth" is used in some places and "elizabeth-line" is used in others but "dlr" is consistent...
STRATFORD_LINES = ("elizabeth-line", "dlr", "tube")

# Read Stratford naptans
STRATFORD_NAPTANS = {}
with open("./data/stratford-naptans.csv", "r") as csvfile:
    naptan_file = csv.reader(csvfile)
    for line_name, naptan in naptan_file:
        STRATFORD_NAPTANS[line_name] = naptan

# Read naptans of terminus stations for all lines passing through Stratford
TERMINI_NAPTANS = {}
with open("./data/terminus-naptans.csv", "r") as csvfile:
    naptan_file = csv.reader(csvfile)
    for row in naptan_file:
        TERMINI_NAPTANS[row[0]] = tuple(row[1:])

# Read bike point IDs
BIKE_POINTS = {}
with open("./data/bike-points.csv", "r") as csvfile:
    naptan_file = csv.reader(csvfile)
    for name, id in naptan_file:
        BIKE_POINTS[name] = id


def _get_next_trains_to_stratford_for_line(line_name: str) -> list:
    """Generates a list of incoming trains to Stratford for a given line.

    Args:
        line_name (str): The line name.

    Returns:
        list: Sorted list of Stratford arrival info for a given line.
    """
    arrivals = []
    for terminus_naptan in TERMINI_NAPTANS[line_name]:
        arrivals += line.getArrivalsByNaptan(
            [line_name], STRATFORD_NAPTANS[line_name], terminus_naptan
        )

    # Sort by timeToStation value for arrival (not actually needed, but keeping it anyway)
    arrivals = sorted(arrivals, key=lambda arrival: arrival["timeToStation"])
    return arrivals


def _n_arrivals_within_5_minutes(arrivals: list[dict]) -> int:
    """Determines the number of trains that will appear within 5 minutes.

    Args:
        arrivals (list[dict]): A list of incoming train info.

    Returns:
        int: The number of trains expected to arrive within 5 minutes.
    """
    return len([arrival for arrival in arrivals if arrival["timeToStation"] < 300])


# Create the objects for doing API calls
line = tflwrapper.line(APP_KEY)
disruptions = tflwrapper.disruptions(APP_KEY)
air_quality = tflwrapper.airQuality(APP_KEY)
roads = tflwrapper.road(APP_KEY)
occupancy = tflwrapper.occupancy(APP_KEY)


def get_tfl_data() -> dict:
    """Get TFL info with the API.

    Returns:
        dict: Current info on broken lifts across TFL, London air quality, number of trains arriving at Stratford, status of the A12, and bike point info.
    """
    data = {}

    # Get number of broken lifts across TFL network
    data["num-broken-lifts"] = len(disruptions.getAllLifts())

    # Get the current air quality data
    data["air-quality"] = air_quality.getAirQuality()["currentForecast"][0][
        "forecastSummary"
    ]

    # Find status of the different lines that pass through Stratford
    statuses = line.getStatusByID(STRATFORD_LINES, True)
    status_info = ""
    for status in statuses:
        if status["id"] in TERMINI_NAPTANS.keys():
            status_info += f" {status['name']} has {len(status['disruptions'])} disruptions and has {status['lineStatuses'][0]['statusSeverityDescription']}."

    # Trim the first space
    data["statford-line-data"] = status_info[1:]

    # Get the number of trains arriving at Stratford within 5 minutes for each line
    n_arrivals = {}
    for line_name in TERMINI_NAPTANS:
        arrivals = _get_next_trains_to_stratford_for_line(line_name)
        n_arrivals[line_name] = _n_arrivals_within_5_minutes(arrivals)

    data["arriving-trains"] = n_arrivals

    # See how the A12 is doing
    a12_info = roads.getByID([A12])[0]
    data["a12-status"] = (
        f"The A12 is currently {a12_info['statusSeverity']} with {a12_info['statusSeverityDescription']}."
    )

    # Get bike point occupancy
    data["bike-points"] = {
        bike_point[
            "name"
        ]: f"{bike_point['totalDocks'] - bike_point['emptyDocks']} out of {bike_point['totalDocks']}"
        for bike_point in occupancy.getBikePointByIDs(BIKE_POINTS.values())
    }

    return data


print(get_tfl_data())
