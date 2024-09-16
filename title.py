import pytermgui as ptg
from pyfiglet import Figlet

f = Figlet(font='gothic')

with ptg.WindowManager() as manager:
    manager.layout.add_slot("Header")
    manager.add(ptg.Window(f.renderText('trafficmancy') + "\n[italic]Look for the sychroniCITY...", box="EMPTY"))