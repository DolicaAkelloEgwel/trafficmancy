import pyxel

from ask_question import ask_question
from traffic_counter import get_traffic_count

APP_WIDTH = 256 * 2
APP_HEIGHT = 144 * 2
PADDING = 20

BOX_WIDTH = APP_WIDTH - PADDING * 2

KEY_MAP = {}

CHARACTER_LIMIT = 117

INSTRUCTIONS = "Submit Question: Enter | Clear: Alt + C (Note - You may have to wait a while, as Trafficmany thinks about your query...)"


def _split_up_long_text(output: str) -> str:
    if len(output) <= CHARACTER_LIMIT:
        return output

    next_line = output[:CHARACTER_LIMIT]
    remaining_text = output[CHARACTER_LIMIT:]

    if "\n" in next_line:
        break_idx = next_line.index("\n")
        return (
            next_line[:break_idx]
            + "\n"
            + _split_up_long_text(next_line[break_idx + 1 :] + remaining_text)
        )

    if remaining_text[0] == " ":
        return next_line + "\n" + _split_up_long_text(remaining_text[1:])

    last_space_idx = next_line.rfind(" ")
    return (
        next_line[:last_space_idx]
        + "\n"
        + _split_up_long_text(next_line[last_space_idx + 1 :] + remaining_text)
    )


class App:
    def __init__(self):
        pyxel.init(APP_WIDTH, APP_HEIGHT, title="Trafficmancy")
        pyxel.load("background.pyxres")
        self.input_text = ""
        self.output_text = " "
        self.partial_text = ""
        self.progress = 1
        self.end = 1
        self.processing_query = False  # Track if typing in input box
        self.count = 0
        pyxel.run(self.update, self.draw)

    def update(self):
        # Handle typing in the input box
        if not self.processing_query:
            for i in range(26):
                if pyxel.btnp(pyxel.KEY_A + i):
                    if pyxel.btn(
                        pyxel.KEY_SHIFT
                    ):  # Check if shift is pressed for uppercase
                        self.input_text += chr(pyxel.KEY_A + i).upper()
                    else:
                        self.input_text += chr(pyxel.KEY_A + i)

            # Handle numbers 0-9
            for i in range(10):
                if not pyxel.btn(pyxel.KEY_SHIFT) and pyxel.btnp(pyxel.KEY_0 + i):
                    self.input_text += chr(pyxel.KEY_0 + i)

            # Handle punctuation symbols using their respective Pyxel key codes
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.input_text += " "
            if pyxel.btnp(pyxel.KEY_SEMICOLON):
                self.input_text += ";"
            if pyxel.btnp(pyxel.KEY_MINUS):
                self.input_text += "-"
            if pyxel.btnp(pyxel.KEY_EQUALS):
                self.input_text += "="
            if pyxel.btnp(pyxel.KEY_BACKSLASH):
                self.input_text += "\\"

            if not pyxel.btn(pyxel.KEY_SHIFT):
                if pyxel.btnp(pyxel.KEY_COMMA):
                    self.input_text += ","
                if pyxel.btnp(pyxel.KEY_PERIOD):
                    self.input_text += "."
                if pyxel.btnp(pyxel.KEY_SLASH):
                    self.input_text += "/"

            # Handle shift-modified symbols for special characters like ?, !, etc.
            if pyxel.btn(pyxel.KEY_SHIFT):
                if pyxel.btnp(pyxel.KEY_1):
                    self.input_text += "!"
                if pyxel.btnp(pyxel.KEY_2):
                    self.input_text += "@"
                if pyxel.btnp(pyxel.KEY_3):
                    self.input_text += "#"
                if pyxel.btnp(pyxel.KEY_4):
                    self.input_text += "$"
                if pyxel.btnp(pyxel.KEY_5):
                    self.input_text += "%"
                if pyxel.btnp(pyxel.KEY_6):
                    self.input_text += "^"
                if pyxel.btnp(pyxel.KEY_7):
                    self.input_text += "&"
                if pyxel.btnp(pyxel.KEY_8):
                    self.input_text += "*"
                if pyxel.btnp(pyxel.KEY_9):
                    self.input_text += "("
                if pyxel.btnp(pyxel.KEY_0):
                    self.input_text += ")"
                if pyxel.btnp(pyxel.KEY_COMMA):
                    self.input_text += "<"
                if pyxel.btnp(pyxel.KEY_PERIOD):
                    self.input_text += ">"
                if pyxel.btnp(pyxel.KEY_SLASH):
                    self.input_text += "?"

        # Handle backspace to remove last character
        if pyxel.btnp(pyxel.KEY_BACKSPACE) and self.input_text:
            self.input_text = self.input_text[:-1]

        # Check for submit button click
        if pyxel.btnp(pyxel.KEY_RETURN):
            traffic_count = get_traffic_count()
            self.output_text = ask_question(self.input_text, traffic_count)
            self.output_text = _split_up_long_text(self.output_text)
            print(self.output_text)
            self.end = len(self.output_text)
            self.progress = 1

    def draw(self):
        pyxel.cls(7)  # Clear screen to white

        pyxel.blt(0, 0, 0, 0, 0, APP_WIDTH, APP_HEIGHT)
        pyxel.blt(APP_WIDTH // 2, 0, 0, 0, 0, APP_WIDTH, APP_HEIGHT)

        pyxel.blt(0, APP_HEIGHT // 2, 0, 0, 0, APP_WIDTH, APP_HEIGHT)
        pyxel.blt(APP_WIDTH // 2, APP_HEIGHT // 2, 0, 0, 0, APP_WIDTH, APP_HEIGHT)

        # Create input box
        pyxel.rect(
            PADDING - 1, 80 - 1, BOX_WIDTH + 2, 12, 8
        )  # Red border for input box
        pyxel.rect(PADDING, 80, BOX_WIDTH, 10, 0)  # Black rectangle for input
        pyxel.text(PADDING + 2, 82, self.input_text, 7)  # Display the input text

        # Create output box
        pyxel.rect(
            PADDING - 1, 100 - 1, BOX_WIDTH + 2, 162, 8
        )  # Red border for output box
        pyxel.rect(PADDING, 100, BOX_WIDTH, 160, 0)  # Black rectangle for output box
        pyxel.text(PADDING + 2, 102, self.partial_text, 7)  # Display user output text

        self.partial_text = self.output_text[: self.progress]

        if self.progress < self.end:
            self.progress += 1

        pyxel.rect(0, APP_HEIGHT - 11, APP_WIDTH, 12, 8)  # Red line for
        pyxel.rect(
            0, APP_HEIGHT - 10, APP_WIDTH, 10, 0
        )  # Black rectangle for output box
        pyxel.text(2, APP_HEIGHT - 8, INSTRUCTIONS, 8)


# Run the application
App()
