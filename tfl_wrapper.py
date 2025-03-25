from collections import namedtuple

import tflwrapper

# Create a namedtuple for station-naptan pair
StationNaptan = namedtuple("StationNaptan", ["name", "naptan"])

# Station Names
STRATFORD = "Stratford"
CENTRAL_TERMINI = [
    "Ealing Broadway",
    "West Ruislip",
    "Grange Hill",
    "Hainault",
    "Epping",
]
ELIZABETH_TERMINI = [
    "Paddington",
    "Shenfield",
    "Heathrow Terminal 5",
    "Liverpool Street",
    "Heathrow Terminal 4",
]
DLR_TERMINI = [
    "Lewisham",
    "Stratford International",
    "Woolwich Arsenal",
    "Canary Wharf",
]

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


def _is_stratford_tube_station(name: str) -> bool:
    """Checks if the station name is actually for Stratford and not Stratford International or Stratford High Street

    Args:
        name (str): The station name.

    Returns:
        bool: True if 'Stratford' is in the name, and 'High Street' and 'International' are not in the name.
    """
    return (
        STRATFORD in name and "High Street" not in name and "International" not in name
    )


def _find_station_naptan_on_line(line_name: str, station_name: str) -> StationNaptan:
    """Finds a station naptan code given a line name and a station name.

    Args:
        line_name (str): The line name.
        station_name (str): The station name.

    Returns:
        StationNaptan: A StationNaptan tuple.
    """
    stop_points = line.getAllStopPoints(line_name)
    naptans = []
    if station_name is not STRATFORD:
        for stop_point in stop_points:
            if station_name in stop_point["commonName"]:
                naptans.append(
                    (station_name, stop_point["naptanId"])
                )  # todo - named tuple
    else:
        for stop_point in stop_points:
            if _is_stratford_tube_station(stop_point["commonName"]):
                naptans.append(
                    (station_name, stop_point["naptanId"])
                )  # todo - named tuple
    print(naptans)
    return naptans


with open("app.key", "r") as f:
    app_key = f.readline()

line = tflwrapper.line(app_key)

# Get the Naptan IDs for Stratford Station on the different lines
for line_name in LINES_THAT_GO_THROUGH_STRATFORD:
    naptans = _find_station_naptan_on_line(line_name, STRATFORD)
    STRATFORD_NAPTANS[line_name] = naptans[0][1]

# Mildmay and Jubilee terminate at Stratford, so just ask for trains that have Stratford as its destination
TERMINI_NAPTANS[MILDMAY].append(STRATFORD_NAPTANS[MILDMAY])
TERMINI_NAPTANS[JUBILEE].append(STRATFORD_NAPTANS[JUBILEE])

# Get Naptans for Central line termini
TERMINI_NAPTANS[CENTRAL] = [
    _find_station_naptan_on_line(CENTRAL, terminus)[0][1]
    for terminus in CENTRAL_TERMINI
]
# Naptans for Elizabeth line termini
TERMINI_NAPTANS[ELIZABETH] = [
    _find_station_naptan_on_line(ELIZABETH, terminus)[0][1]
    for terminus in ELIZABETH_TERMINI
]
# Naptans for DLR termini
TERMINI_NAPTANS[DLR] = [
    _find_station_naptan_on_line(DLR, terminus)[0][1] for terminus in DLR_TERMINI
]

# Find info on trains heading to/from Stratford
for line_name in TERMINI_NAPTANS:
    for terminus_naptan in TERMINI_NAPTANS[line_name]:
        arrivals = line.getArrivalsByNaptan(
            [line_name], STRATFORD_NAPTANS[line_name], terminus_naptan
        )[:1]
        if not arrivals:
            print(line_name, terminus_naptan)


def get_tfl_data():
    data = {}

    # Get number of broken lifts across TFL network
    disruptions = tflwrapper.disruptions(app_key)
    data["num-broken-lifts"] = len(disruptions.getAllLifts())

    # Get today's air quality data
    air_quality = tflwrapper.airQuality(app_key)
    data["air-quality"] = air_quality.getAirQuality()["currentForecast"][0][
        "forecastSummary"
    ]

    # Find status of the different lines that pass through Stratford
    line = tflwrapper.line(app_key)
    statuses = line.getStatusByID(STRATFORD_LINES, True)
    status_info = ""
    for status in statuses:
        if status["id"] in LINES_THAT_GO_THROUGH_STRATFORD:
            status_info += f" {status['name']} has {len(status['disruptions'])} disruptions and has {status['lineStatuses'][0]['statusSeverityDescription']}."

    data["statford-line-data"] = status_info[1:]

    return data


print(get_tfl_data())
