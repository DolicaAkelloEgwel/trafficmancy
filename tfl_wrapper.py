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

with open("app.key", "r") as f:
    app_key = f.readline()

bike_point = tflwrapper.bikePoint(app_key)

crowding = tflwrapper.crowding(app_key)

for naptan in STRATFORD_NAPTANS:
    for crowd in crowding.getAllByNaptan(naptan):
        print(crowd)

line = tflwrapper.line(app_key)

for naptan in STRATFORD_NAPTANS:
    print(
        line.getTimetableFromStation(
            _line="central", NaPTANID=naptan, direction="outbound"
        )
    )


def get_tfl_data():
    data = {}

    disruptions = tflwrapper.disruptions(app_key)
    data["num-broken-lifts"] = len(disruptions.getAllLifts())

    air_quality = tflwrapper.airQuality(app_key)
    data["air-quality"] = air_quality.getAirQuality()["currentForecast"][0][
        "forecastSummary"
    ]

    return data
