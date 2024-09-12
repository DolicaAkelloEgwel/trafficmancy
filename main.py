import time

import pytermgui as ptg
from ask_question import ask_question

COOL_LOGO = []

with open("ascii-logo", "r") as file:
    COOL_LOGO = file.read()
    print(COOL_LOGO)

with ptg.WindowManager() as manager:
    manager.layout.add_slot("Header")
    header = ptg.Window(
        COOL_LOGO,
    )
    manager.add(header)

    manager.layout.add_slot("Body")
    input_area = ptg.Window(
        ptg.Label("Enter Your Query:"), ptg.InputField("", prompt=""), box="DOUBLE"
    )
    manager.add(input_area)

    manager.run()
