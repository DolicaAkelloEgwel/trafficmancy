import tflwrapper

STRATFORD_NAPTANS = ["9400ZZLUSTD","9400ZZLUSTD1","9400ZZLUSTD2","9400ZZLUSTD3","9400ZZLUSTD4","9400ZZLUSTD5","9400ZZLUSTD6"]

with open("app.key", "r") as f:
    app_key = f.readline()

disruptions = tflwrapper.disruptions(app_key)
for lift in disruptions.getAllLifts():
    print(lift)

# print(tflwrapper.line.getArrivalsByNaptan(lineids=["central", "dlr", "elizabeth", "jubilee", "mildmay"], naptan="940GZZLUSTD", destinationStationId=""))

crowding = tflwrapper.crowding(app_key)

for naptan in STRATFORD_NAPTANS:
    for crowd in crowding.getAllByNaptan(naptan):
        print(crowd)

line = tflwrapper.line(app_key)

print(line.getTimetableFromStation(_line = "central", NaPTANID=STRATFORD_NAPTANS[0], direction="outbound"))

def get_tfl_data():
    pass
