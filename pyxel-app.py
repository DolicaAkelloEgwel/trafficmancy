import pyxel
from traffic_counter import get_traffic_count
from ask_question import ask_question

APP_WIDTH = 256 * 2
APP_HEIGHT = 144 * 2
PADDING = 20

BOX_WIDTH = APP_WIDTH - PADDING * 2

PROCESSING_TEXT = "Processing"

KEY_MAP = {}



class App:
    def __init__(self):
        pyxel.init(APP_WIDTH, APP_HEIGHT, title="Trafficmancy")
        pyxel.load("background.pyxres")
        self.input_text = ""
        self.output_text = ""
        self.processing_query = False  # Track if typing in input box
        self.count = 0
        pyxel.run(self.update, self.draw)

    def update(self):
        # Handle typing in the input box
        if not self.processing_query:
            for i in range(26):
                if pyxel.btnp(pyxel.KEY_A + i):
                    if pyxel.btn(pyxel.KEY_SHIFT):  # Check if shift is pressed for uppercase
                        self.input_text += chr(pyxel.KEY_A + i).upper()
                    else:
                        self.input_text += chr(pyxel.KEY_A + i)

            # Handle numbers 0-9
            for i in range(10):
                if pyxel.btnp(pyxel.KEY_0 + i):
                    self.input_text += chr(pyxel.KEY_0 + i)

            # Handle punctuation symbols using their respective Pyxel key codes
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.input_text += ' '
            if pyxel.btnp(pyxel.KEY_COMMA):
                self.input_text += ','
            if pyxel.btnp(pyxel.KEY_PERIOD):
                self.input_text += '.'
            if pyxel.btnp(pyxel.KEY_SLASH):
                self.input_text += '/'
            if pyxel.btnp(pyxel.KEY_SEMICOLON):
                self.input_text += ';'
            if pyxel.btnp(pyxel.KEY_MINUS):
                self.input_text += '-'
            if pyxel.btnp(pyxel.KEY_EQUALS):
                self.input_text += '='
            if pyxel.btnp(pyxel.KEY_BACKSLASH):
                self.input_text += '\\'

            # Handle shift-modified symbols for special characters like ?, !, etc.
            if pyxel.btn(pyxel.KEY_SHIFT):
                if pyxel.btnp(pyxel.KEY_1):
                    self.input_text += '!'
                if pyxel.btnp(pyxel.KEY_2):
                    self.input_text += '@'
                if pyxel.btnp(pyxel.KEY_3):
                    self.input_text += '#'
                if pyxel.btnp(pyxel.KEY_4):
                    self.input_text += '$'
                if pyxel.btnp(pyxel.KEY_5):
                    self.input_text += '%'
                if pyxel.btnp(pyxel.KEY_6):
                    self.input_text += '^'
                if pyxel.btnp(pyxel.KEY_7):
                    self.input_text += '&'
                if pyxel.btnp(pyxel.KEY_8):
                    self.input_text += '*'
                if pyxel.btnp(pyxel.KEY_9):
                    self.input_text += '('
                if pyxel.btnp(pyxel.KEY_0):
                    self.input_text += ')'
                if pyxel.btnp(pyxel.KEY_COMMA):
                    self.input_text += '<'
                if pyxel.btnp(pyxel.KEY_PERIOD):
                    self.input_text += '>'
                if pyxel.btnp(pyxel.KEY_SLASH):
                    self.input_text += '?'

        # Handle backspace to remove last character
        if pyxel.btnp(pyxel.KEY_BACKSPACE) and self.input_text:
            self.input_text = self.input_text[:-1]

        # Check for submit button click
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.output_text = PROCESSING_TEXT + "..."
            traffic_count = get_traffic_count()
            self.output_text = ask_question(self.input_text, traffic_count)

    def draw(self):
        pyxel.cls(7)  # Clear screen to white

        pyxel.blt(0, 0, 0, 0, 0, APP_WIDTH, APP_HEIGHT)
        pyxel.blt(APP_WIDTH // 2, 0, 0, 0, 0, APP_WIDTH, APP_HEIGHT)

        pyxel.blt(0, APP_HEIGHT // 2, 0, 0, 0, APP_WIDTH, APP_HEIGHT)
        pyxel.blt(APP_WIDTH // 2, APP_HEIGHT // 2, 0, 0, 0, APP_WIDTH, APP_HEIGHT)

        # Create input box
        pyxel.rect(PADDING, 80, BOX_WIDTH, 10, 0)  # Black rectangle for input
        pyxel.text(PADDING + 2, 82, self.input_text, 7)  # Display the input text

        # Create output box
        pyxel.rect(PADDING, 110, BOX_WIDTH, 150, 0)  # Black rectangle for output box
        pyxel.text(PADDING + 2, 115, self.output_text, 7)  # Display user output text


# Run the application
App()
