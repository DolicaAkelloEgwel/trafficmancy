from asciimatics.effects import Cycle, Print
from asciimatics.renderers import FigletText, StaticRenderer
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError
import sys

SUBTITLE = "Look at the sychroniCITY..."

def demo(screen):
    effects = [
        # Figlet animated title
        Cycle(
            screen,
            FigletText("trafficmancy", font='gothic'),
            screen.height // 2 - 8
        ),
        # Plain centered text beneath the Figlet logo
        Print(
            screen,
            StaticRenderer([SUBTITLE]),  # Your plain text
            y=screen.height // 2,  # Position below the Figlet text
            x=(screen.width - len(SUBTITLE)) // 2,  # Center the text horizontally
            transparent=False,
            start_frame=0,
            stop_frame=0  # Ensures it stays visible throughout the scene
        )
    ]

    screen.play([Scene(effects, 500)])

Screen.wrapper(demo)
