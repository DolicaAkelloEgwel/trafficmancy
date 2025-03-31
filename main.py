import os

import ollama
import pyxel

LOREM_IPSUM = False
DEPTHAI = False

TRAFFICMANCY_INITIAL_PROMPT = ""

PROJECT_PATH = os.path.dirname(os.path.realpath(__file__))
TEXT_PATH = os.path.join(PROJECT_PATH, "text")

if LOREM_IPSUM:

    WHAT_IS_BEING_USED = "nothing"
    with open(os.path.join(TEXT_PATH, "lorem-ipsum"), "r") as f:
        LOREM_IPSUM = f.read()

    dummy_reponse = [
        {"message": {"content": word + " "}} for word in LOREM_IPSUM.split(" ")
    ]

    def ask_question(query: str):
        return iter(dummy_reponse)

elif DEPTHAI:
    from stereo_camera import get_traffic_count

    WHAT_IS_BEING_USED = "the flow of the traffic outside"
    with open(os.path.join(TEXT_PATH, "camera-prompt"), "r") as f:
        TRAFFICMANCY_INITIAL_PROMPT += f.read()

    def ask_question(query: str):
        """Asks Ollama a question based on the traffic observations from the camera.

        Args:
            query (str): The user's query.

        Returns:
            _type_: _description_
        """
        counts = get_traffic_count()
        query = (
            f'{TRAFFICMANCY_INITIAL_PROMPT}. {counts["car"]} cars, {counts["person"]} pedestrians,'
            f' {counts["bus"]} buses, {counts["motorbike"]} motorbikes, and {counts["bicycle"]} cyclists were observed.'
            " Based on this snapshot, analyse the observed elements and provide a symbolic interpretation that answers"
            f" the following query: {query}"
        )
        stream = ollama.chat(
            model=MODEL,
            messages=[{"role": "user", "content": query}],
            stream=True,
        )
        return stream

else:
    from tfl_wrapper import get_tfl_data

    WHAT_IS_BEING_USED = "live TFL data"
    with open(os.path.join(TEXT_PATH, "tfl-prompt"), "r") as f:
        TRAFFICMANCY_INITIAL_PROMPT += f.read()

    def ask_question(query: str):
        """Asks Ollama a question based on TFL data.

        Args:
            query (str): The user's query.

        Returns:
            _type_: _description_
        """
        tfl_data = get_tfl_data()
        query = (
            f"{TRAFFICMANCY_INITIAL_PROMPT}. There are currently {tfl_data['num-broken-lifts']} broken lifts across the"
            f" entire TFL network. This is the current air quality report for London: {tfl_data['air-quality']}. These"
            " are the statuses for the different lines connected to Stratford Station:"
            f" {tfl_data['stratford-line-data']}. The total number of trains across all lines expected to arrive at"
            f" Stratford Station within the next five minutes is {tfl_data['arriving-trains']}. This is the current"
            f" status of the A12 road: {tfl_data['a12-status']}. This is the current data on number of available bikes"
            f" for the nearby bike points: {tfl_data['bike-points']}. Based on this snapshot, analyse the observed"
            f" elements and provide a symbolic interpretation that answers the following query: {query}"
        )
        stream = ollama.chat(
            model=MODEL,
            messages=[{"role": "user", "content": query}],
            stream=True,
        )
        return stream


APP_WIDTH = 256 * 2
APP_HEIGHT = 144 * 2
PADDING = 20

BOX_WIDTH = APP_WIDTH - PADDING * 2

CHARACTER_LIMIT = 117
MAX_LINES = 29

INSTRUCTIONS = (
    "Submit Question: Enter | Scroll: Up/Down | Toggle Info: Alt + i | Clear: Alt + c"
)

INFO_INPUT = "Look for the synchroniCITY...".center(CHARACTER_LIMIT)

with open(os.path.join(TEXT_PATH, "info"), "r") as f:
    INFO_OUTPUT = (
        f"INSTRUCTIONS: Type a question and hit Enter. Trafficmancy will then consult {WHAT_IS_BEING_USED} to answer your query.\n\n"
        + f.read()
    )

TITLE = "Trafficmancy"
NEW_LINE = "\n"

INPUT_BOX_Y = 60
INPUT_BOX_HEIGHT = 10

OUTPUT_BOX_Y = INPUT_BOX_Y + 20
OUTPUT_BOX_HEIGHT = 184

TITLE_Y = 16

MODEL = "dolphin-phi"


def _split_up_long_text(output: str, character_limit: int) -> str:
    # when was the last time I used recursion ???

    if len(output) <= character_limit:
        return output

    next_line = output[:character_limit]
    remaining_text = output[character_limit:]

    if NEW_LINE in next_line:
        break_idx = next_line.index(NEW_LINE)
        return (
            next_line[:break_idx]
            + NEW_LINE
            + _split_up_long_text(
                next_line[break_idx + 1 :] + remaining_text, character_limit
            )
        )

    if remaining_text[0] == " ":
        return (
            next_line
            + NEW_LINE
            + _split_up_long_text(remaining_text[1:], character_limit)
        )

    last_space_idx = next_line.rfind(" ")
    return (
        next_line[:last_space_idx]
        + NEW_LINE
        + _split_up_long_text(
            next_line[last_space_idx + 1 :] + remaining_text, character_limit
        )
    )


class Page:
    def __init__(self, text: str = ""):
        self._text = text
        self._progress = 0

    def can_add_word(self, word: str) -> bool:
        if len(self.lines) < MAX_LINES:
            return True
        return len(self.lines[-1] + word) < CHARACTER_LIMIT

    def to_str(self) -> str:
        return self._text[: self._progress]

    def add_word(self, word: str):
        if len(self.lines[-1] + word) > CHARACTER_LIMIT:
            if word[0] == " ":
                word = word[1:]
            self._text += "\n" + word
        elif not self._text and word[0] == " ":
            self._text += word[1:]
        else:
            self._text += word

    @property
    def lines(self) -> list[str]:
        return self._text.split("\n")

    @property
    def progress(self) -> int:
        return self._progress

    @property
    def incomplete(self) -> bool:
        return self._progress < len(self._text)

    @progress.setter
    def progress(self, p: int):
        self._progress = p

    @property
    def is_empty(self) -> bool:
        return not self._text

    def clear(self):
        self._text = ""
        self._progress = 0


class ResponseText:

    def __init__(self):
        self._pages = [Page(), Page(), Page()]
        self._idx = 0

    def add_word(self, word: str):
        print(word)
        for i in range(len(self._pages)):
            if self._pages[i].can_add_word(word):
                if (
                    i < len(self._pages) - 1 and self._pages[i + 1].is_empty
                ) or i == len(self._pages):
                    self._pages[i].add_word(word)
                    return

    def to_str(self):
        return self._pages[self._idx].to_str()

    @property
    def current_page(self):
        return self._pages[self._idx]

    @property
    def idx(self):
        return self._idx

    @idx.setter
    def idx(self, i: int):
        if i >= len(self._pages) or i < 0:
            return
        if self._pages[i].is_empty:
            return
        self._idx = i

    @property
    def is_empty(self) -> bool:
        return all([page.is_empty for page in self._pages])

    def clear(self):
        for page in self._pages:
            page.clear()
        self.idx = 0


def _get_character() -> str:
    """Gets the character to display on the input field.

    Returns:
        str: A single-letter string for the character that needs to be added to the query field. Or nothing if the character isn't recognised.
    """

    # Handle the letters of the alphabet
    for i in range(26):
        if pyxel.btnp(pyxel.KEY_A + i):
            if pyxel.btn(pyxel.KEY_SHIFT):
                return chr(pyxel.KEY_A + i).upper()
            else:
                return chr(pyxel.KEY_A + i)

    # Handle numbers 0-9
    for i in range(10):
        if not pyxel.btn(pyxel.KEY_SHIFT) and pyxel.btnp(pyxel.KEY_0 + i):
            return chr(pyxel.KEY_0 + i)

    if pyxel.btnp(pyxel.KEY_SPACE):
        return " "

    # Handle symbols without shfit key
    if not pyxel.btn(pyxel.KEY_SHIFT):
        if pyxel.btnp(pyxel.KEY_COMMA):
            return ","
        if pyxel.btnp(pyxel.KEY_PERIOD):
            return "."
        if pyxel.btnp(pyxel.KEY_SLASH):
            return "/"
        if pyxel.btnp(pyxel.KEY_EQUALS):
            return "="
        if pyxel.btnp(pyxel.KEY_SEMICOLON):
            return ";"
        if pyxel.btnp(pyxel.KEY_MINUS):
            return "-"
        if pyxel.btnp(pyxel.KEY_BACKSLASH):
            return "\\"

    # Handle shift-modified symbols for special characters like ?, !, etc.
    if pyxel.btnp(pyxel.KEY_1):
        return "!"
    if pyxel.btnp(pyxel.KEY_2):
        return '"'
    if pyxel.btnp(pyxel.KEY_3):
        return "£"
    if pyxel.btnp(pyxel.KEY_4):
        return "$"
    if pyxel.btnp(pyxel.KEY_5):
        return "%"
    if pyxel.btnp(pyxel.KEY_6):
        return "^"
    if pyxel.btnp(pyxel.KEY_7):
        return "&"
    if pyxel.btnp(pyxel.KEY_8):
        return "*"
    if pyxel.btnp(pyxel.KEY_9):
        return "("
    if pyxel.btnp(pyxel.KEY_0):
        return ")"
    if pyxel.btnp(pyxel.KEY_COMMA):
        return "<"
    if pyxel.btnp(pyxel.KEY_PERIOD):
        return ">"
    if pyxel.btnp(pyxel.KEY_SLASH):
        return "?"
    if pyxel.btnp(pyxel.KEY_EQUALS):
        return "+"
    if pyxel.btnp(pyxel.KEY_SEMICOLON):
        return ":"
    if pyxel.btnp(pyxel.KEY_MINUS):
        return "_"
    if pyxel.btnp(pyxel.KEY_BACKSLASH):
        return "|"

    return ""


INFO_OUTPUT = _split_up_long_text(INFO_OUTPUT, CHARACTER_LIMIT)


class App:
    def __init__(self):
        pyxel.init(APP_WIDTH, APP_HEIGHT, title=TITLE, quit_key=pyxel.KEY_NONE)
        pyxel.load(os.path.join(PROJECT_PATH, "background.pyxres"))

        self.stream = None
        self.ollama_text = ResponseText()
        self.input_text = ""

        self.info_mode = False
        self.wizard = pyxel.Font(os.path.join(PROJECT_PATH, "wizard.bdf"))

        pyxel.run(self.update, self.draw)

    def update(self):

        # Toggle info mode
        if pyxel.btnp(pyxel.KEY_LALT, True, 1) and pyxel.btnp(pyxel.KEY_I):
            self.info_mode = not self.info_mode
            return

        # Do nothing if we're in info mode
        if self.info_mode:
            return

        # Clear the screen
        if pyxel.btnp(pyxel.KEY_LALT, True, 1) and pyxel.btnp(pyxel.KEY_C):
            self.input_text = ""
            self.ollama_text.clear()
            return

        if not self.ollama_text.current_page.incomplete:
            # Only allow scrolling when the message is finished
            if pyxel.btnp(pyxel.KEY_UP):
                self.ollama_text.idx -= 1

            if pyxel.btnp(pyxel.KEY_DOWN):
                self.ollama_text.idx += 1

        # Add a character to the input box - don't bother if we've passed the limit (tough if the question is too long)
        if len(self.input_text) < CHARACTER_LIMIT:
            self.input_text += _get_character()

        # Handle backspace to remove last character
        if self.input_text:
            if pyxel.btnp(pyxel.KEY_BACKSPACE, False):
                self.input_text = self.input_text[:-1]

        # Generate a reply when the user hits Enter
        if pyxel.btnp(pyxel.KEY_RETURN) and self.input_text:
            self.ollama_text.clear()
            self.stream = ask_question(self.input_text)

        if self.stream is not None:
            try:
                chunk = next(self.stream)
                word = chunk["message"]["content"]
                self.ollama_text.add_word(word)
            except StopIteration:
                self.stream = None

    def draw(self):
        # Clear the screen
        pyxel.cls(7)

        # Fill with the background image (funky bus seat pattern)
        pyxel.blt(0, 0, 0, 0, 0, APP_WIDTH, APP_HEIGHT)
        pyxel.blt(APP_WIDTH // 2, 0, 0, 0, 0, APP_WIDTH, APP_HEIGHT)
        pyxel.blt(0, APP_HEIGHT // 2, 0, 0, 0, APP_WIDTH, APP_HEIGHT)
        pyxel.blt(APP_WIDTH // 2, APP_HEIGHT // 2, 0, 0, 0, APP_WIDTH, APP_HEIGHT)

        # Display the title + a "border"
        pyxel.text(161, TITLE_Y, TITLE, 8, self.wizard)
        pyxel.text(160, TITLE_Y - 1, TITLE, 8, self.wizard)
        pyxel.text(160, TITLE_Y + 1, TITLE, 8, self.wizard)
        pyxel.text(159, TITLE_Y, TITLE, 8, self.wizard)
        pyxel.text(160, TITLE_Y, TITLE, 0, self.wizard)

        # Create input box
        pyxel.rect(
            PADDING - 1, INPUT_BOX_Y - 1, BOX_WIDTH + 2, INPUT_BOX_HEIGHT + 2, 8
        )  # Red border for input box
        pyxel.rect(
            PADDING, INPUT_BOX_Y, BOX_WIDTH, INPUT_BOX_HEIGHT, 0
        )  # Black rectangle for input

        # Create output box
        pyxel.rect(
            PADDING - 1,
            OUTPUT_BOX_Y - 1,
            BOX_WIDTH + 2,
            OUTPUT_BOX_HEIGHT + 2,
            8,
        )  # Red border for output box
        pyxel.rect(
            PADDING, OUTPUT_BOX_Y, BOX_WIDTH, OUTPUT_BOX_HEIGHT, 0
        )  # Black rectangle for output box

        if self.info_mode:
            pyxel.text(
                PADDING + 2, INPUT_BOX_Y + 2, INFO_INPUT, pyxel.frame_count % 15
            )  # This is just fun

            pyxel.text(
                PADDING + 2, OUTPUT_BOX_Y + 2, INFO_OUTPUT, 7
            )  # Info about my project
        else:
            pyxel.text(
                PADDING + 2, INPUT_BOX_Y + 2, self.input_text, 7
            )  # Display the input text

            pyxel.text(
                PADDING + 2, OUTPUT_BOX_Y + 2, self.ollama_text.to_str(), 7
            )  # Display user output text

            # Increase the counter for the output text display - unless we're already at the end
            if self.ollama_text.current_page.incomplete:
                self.ollama_text.current_page.progress += 1

        pyxel.rect(
            0, APP_HEIGHT - 11, APP_WIDTH, 12, 8
        )  # Red line for instructions footer
        pyxel.rect(
            0, APP_HEIGHT - 10, APP_WIDTH, 10, 0
        )  # Black rectangle for instructions footer

        # Commands text at the bottom
        pyxel.text(2, APP_HEIGHT - 8, INSTRUCTIONS, 8)


# Run the application
App()
