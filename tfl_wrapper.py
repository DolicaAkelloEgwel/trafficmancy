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

# Line Names
CENTRAL = "central"
ELIZABETH = "elizabeth"
MILDMAY = "mildmay"

STRATFORD_BIKE_POINT_ID = "BikePoints_790"
STRATFORD_LINES = ["elizabeth-line", "dlr", "tube"]
STATUS_NAMES = [ELIZABETH, "dlr", CENTRAL, MILDMAY, "jubilee"]
STRATFORD_NAPTANS = {name: None for name in STATUS_NAMES}
DEST_NAPTANS = {line_name: [] for line_name in STATUS_NAMES}


def _is_stratford_tube_station(name: str) -> bool:
    """ """
    return (
        STRATFORD in name and "High Street" not in name and "International" not in name
    )


def _find_station_naptan_on_line(line_name: str, station_name: str):
    """ """
    stop_points = line.getAllStopPoints(line_name)
    naptans = []
    for stop_point in stop_points:
        if station_name in stop_point["commonName"]:
            naptans.append((station_name, stop_point["naptanId"]))  # todo - named tuple
    return naptans


with open("app.key", "r") as f:
    app_key = f.readline()

line = tflwrapper.line(app_key)

# Get the Naptan IDs for Stratford Station
for line_name in STATUS_NAMES:
    naptans = _find_station_naptan_on_line(line_name, STRATFORD)
    naptans = [naptan for naptan in naptans if _is_stratford_tube_station(naptan[0])][0]
    STRATFORD_NAPTANS[line_name] = naptans[1]

DEST_NAPTANS[MILDMAY].append(STRATFORD_NAPTANS[MILDMAY])
DEST_NAPTANS["jubilee"].append(STRATFORD_NAPTANS["jubilee"])

# Get the Naptan IDs for Central line stops around Stratford
DEST_NAPTANS[CENTRAL] = [
    _find_station_naptan_on_line(CENTRAL, terminus)[0][1]
    for terminus in CENTRAL_TERMINI
]

DEST_NAPTANS["elizabeth"] = [
    _find_station_naptan_on_line("elizabeth", "Paddington")[0][1],
    _find_station_naptan_on_line("elizabeth", "Shenfield")[0][1],
    _find_station_naptan_on_line("elizabeth", "Heathrow Terminal 5")[0][1],
    _find_station_naptan_on_line("elizabeth", "Liverpool Street")[0][1],
    _find_station_naptan_on_line("elizabeth", "Heathrow Terminal 4")[0][1],
]
DEST_NAPTANS["dlr"] = [
    _find_station_naptan_on_line("dlr", "Lewisham")[0][1],
    _find_station_naptan_on_line("dlr", "Stratford International")[0][1],
    _find_station_naptan_on_line("dlr", "Woolwich Arsenal")[0][1],
    _find_station_naptan_on_line("dlr", "Canary Wharf")[0][1],
]

for line_name in DEST_NAPTANS:
    for dest_naptan in DEST_NAPTANS[line_name]:
        print(dest_naptan)
        arrivals = line.getArrivalsByNaptan(
            [line_name], STRATFORD_NAPTANS[line_name], dest_naptan
        )[:1]
        print(arrivals)


def get_tfl_data():
    data = {}

    disruptions = tflwrapper.disruptions(app_key)
    data["num-broken-lifts"] = len(disruptions.getAllLifts())

    air_quality = tflwrapper.airQuality(app_key)
    data["air-quality"] = air_quality.getAirQuality()["currentForecast"][0][
        "forecastSummary"
    ]

    line = tflwrapper.line(app_key)
    statuses = line.getStatusByID(STRATFORD_LINES, True)
    status_info = ""
    for status in statuses:
        if status["id"] in STATUS_NAMES:
            status_info += f" {status['name']} has {len(status['disruptions'])} disruptions and has {status['lineStatuses'][0]['statusSeverityDescription']}."

    data["statford-line-data"] = status_info[1:]

    return data
