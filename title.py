import pytermgui as ptg
from pyfiglet import Figlet

f = Figlet(font='doom')

with ptg.WindowManager() as manager:
    manager.layout.add_slot("Header")
    manager.add(ptg.Window(f.renderText('trafficmancy')))