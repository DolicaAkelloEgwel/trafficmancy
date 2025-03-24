import tflwrapper

STRATFORD_BIKE_POINT_ID = "BikePoints_790"
STRATFORD_LINES = ["elizabeth-line", "dlr", "tube"]
STATUS_NAMES = ["elizabeth", "dlr", "central", "mildmay", "jubilee"]
STRATFORD_NAPTANS = {name: None for name in STATUS_NAMES}


def _is_stratford_tube_station(name: str) -> bool:
    return (
        "Stratford" in name
        and "High Street" not in name
        and "International" not in name
    )


with open("app.key", "r") as f:
    app_key = f.readline()

line = tflwrapper.line(app_key)

# Get the Naptan IDs for Stratford Station
for name in STATUS_NAMES:
    stop_points = line.getAllStopPoints(name)
    for stop_point in stop_points:
        if _is_stratford_tube_station(stop_point["commonName"]):
            STRATFORD_NAPTANS[name] = stop_point["naptanId"]


def _get_arrival_with_naptan(line_name: str, naptan: str):
    if line_name in ["mildmay", "jubilee"]:
        return line.getArrivalsByNaptan(
            [line_name], STRATFORD_NAPTANS[line_name], STRATFORD_NAPTANS[line_name]
        )
    else:
        return []


for line_name in STRATFORD_NAPTANS:
    print(_get_arrival_with_naptan(line_name, STRATFORD_NAPTANS[line_name])[:5])


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
