import tflwrapper

STRATFORD_NAPTANS = [
    "9400ZZLUSTD",
    "9400ZZLUSTD1",
    "9400ZZLUSTD2",
    "9400ZZLUSTD3",
    "9400ZZLUSTD4",
    "9400ZZLUSTD5",
    "9400ZZLUSTD6",
]
STRATFORD_BIKE_POINT_ID = "BikePoints_790"
STRATFORD_LINES = ["elizabeth-line", "dlr", "tube"]
STATUS_NAMES = ["elizabeth", "dlr", "central", "jubilee"]

with open("app.key", "r") as f:
    app_key = f.readline()

line = tflwrapper.line(app_key)

statuses = line.getStatusByID(STRATFORD_LINES + ["tube"], True)
status_info = ""
for status in statuses:
    if status["id"] in STATUS_NAMES:
        status_info += f" {status['name']} has {len(status['disruptions'])} disruptions and has {status['lineStatuses'][0]['statusSeverityDescription']}."

status_info = status_info[1:]


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
