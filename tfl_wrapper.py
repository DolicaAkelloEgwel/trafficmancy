import tflwrapper

with open("app.key", "r") as f:
    app_key = f.readline()

disruptions = tflwrapper.disruptions(app_key)
for lift in disruptions.getAllLifts():
    print(lift)
