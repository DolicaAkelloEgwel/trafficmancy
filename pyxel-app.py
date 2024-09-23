import pyxel

TESTING = True

if TESTING:

    def ask_question(arg1, arg2):
        return (
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus sed consectetur mauris. Aenean nec ex turpis. "
            "Quisque accumsan ex a enim ultrices, a pretium sem hendrerit. Phasellus facilisis, nunc ut accumsan pulvinar, "
            "velit mi pellentesque orci, et ullamcorper eros ante sit amet ipsum. Duis et libero pulvinar, eleifend orci vel, "
            "suscipit nisl. Phasellus faucibus tempor quam vel viverra. Mauris consequat porttitor augue, a ornare nunc commodo "
            "pellentesque. Interdum et malesuada fames ac ante ipsum primis in faucibus.\n\n"
            "Nam ut imperdiet dolor. Duis eget tristique sapien, condimentum molestie erat. Phasellus rhoncus accumsan metus. "
            "Etiam tristique congue semper. Donec ultricies orci ante, laoreet dignissim mauris tincidunt et. In maximus finibus "
            "dolor sit amet fermentum. Nunc feugiat, orci eget bibendum viverra, est magna rhoncus metus, euismod placerat turpis "
            "nisi in sapien. Vivamus imperdiet, nisl quis venenatis aliquet, arcu sapien consectetur lorem, eu tempor risus nisi "
            "sit amet ante. Praesent sagittis finibus ex, euismod volutpat urna tincidunt sed. Praesent quis dignissim nisl. "
            "Maecenas dapibus ante eros. Donec iaculis velit augue, ut pulvinar lacus consequat et.\n\n"
            "Aenean a libero elit. Nam fringilla dolor id justo sodales convallis. In dapibus, dolor quis tincidunt euismod, eros "
            "risus gravida urna, sit amet finibus tortor mauris et nunc. Aenean dolor augue, sodales sit amet volutpat quis, "
            "fringilla quis est. Integer ante ipsum, semper id ex iaculis, auctor blandit elit. Integer urna tellus, bibendum "
            "vitae finibus eu, aliquam eu felis. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos "
            "himenaeos. Nullam laoreet finibus velit, sit amet lacinia massa interdum sit amet. Nam gravida ornare risus, in "
            "molestie tellus mattis sit amet. Aenean a ante libero. Mauris vulputate augue nec est egestas, vitae imperdiet urna "
            "tempor.\n\n"
            "Aliquam neque leo, posuere ac tortor vitae, dictum pellentesque urna. Suspendisse potenti. Fusce faucibus neque vitae "
            "quam porta elementum. Aliquam placerat libero eu elit vehicula tristique sed at mi. Proin facilisis ante dolor, quis "
            "commodo leo facilisis id. Fusce varius, orci sit amet accumsan vestibulum, augue ex pharetra est, at sagittis eros "
            "magna nec nunc. Aliquam laoreet risus nec massa vehicula, sit amet cursus turpis varius. Nullam imperdiet a odio vitae "
            "vulputate. Vivamus aliquam sed metus sed mattis.\n\n"
            "Pellentesque laoreet mi at dolor porta, ut aliquet ipsum laoreet. Aenean eleifend nisl eros, eget viverra leo blandit "
            "sed. Nullam convallis, ligula efficitur viverra maximus, tellus risus posuere dolor, id ultrices est orci dignissim "
            "libero. Sed sed lectus congue, interdum risus non, euismod augue. Vestibulum in venenatis urna. Integer nec nunc arcu. "
            "Ut a libero ornare, condimentum ante ac, auctor nisl. Vestibulum rutrum pellentesque eros sed egestas. Nunc vulputate "
            "velit vitae purus vestibulum, non bibendum lectus aliquam.\n\n"
        )

    def get_traffic_count():
        return None

else:
    from ask_question import ask_question
    from traffic_counter import get_traffic_count

APP_WIDTH = 256 * 2
APP_HEIGHT = 144 * 2
PADDING = 20

BOX_WIDTH = APP_WIDTH - PADDING * 2

CHARACTER_LIMIT = 117

INSTRUCTIONS = "Submit Question: Enter | Clear: Alt + c | Toggle Info: Alt + i"

INFO_INPUT = "Look for the synchroniCITY...".center(CHARACTER_LIMIT)
INFO_OUTPUT = "INSTRUCTIONS: Type a question and hit Enter. Trafficmancy will then consult the flow of the traffic outside to answer your query.\n\nTrafficmancy was a little thing I put together so that I could say I contributed something to all of this. I'm not an artist (yet...?) and I never even heard people talk about `practices` before starting this role.\n\nTech-wise, the responses you're getting are coming from the Ollama dolphin-phi model that is running entirely on the little machine on the left, and the camera is being used to count how many people/cars/etc move past in a ten second period. The interface was made with a Python library called pyxel that weirdly doesn't seem to accept the existence of the pound symbol?\n\nThe inspiration from this partly came from a schizophrenic Rosicrucian guy who told me he could receive information about the future from absolutely anything. If birds started chirping or a helicopter flew overhead, he was able to see how these were messages from the divine. Perhaps you could call that panmancy? Anyways, we stopped talking when his invisible helpers told him that my astral self had done bad things on the other side. \n\nAlso, this machine may freeze at times, in which case you'll have to ask me to reset the device."

TITLE = "Trafficmancy"

INPUT_BOX_Y = 60
INPUT_BOX_HEIGHT = 10

OUTPUT_BOX_Y = INPUT_BOX_Y + 20
OUTPUT_BOX_HEIGHT = 184

TITLE_Y = 16


def _get_character() -> str:

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


INFO_OUTPUT = _split_up_long_text(INFO_OUTPUT)


class App:
    def __init__(self):
        pyxel.init(APP_WIDTH, APP_HEIGHT, title=TITLE, quit_key=pyxel.KEY_NONE)
        pyxel.load("background.pyxres")
        self.input_text = ""
        self.output_text = " "
        self.partial_text = ""
        self.progress = 1
        self.end = 1
        self.info_mode = False
        self.wizard = pyxel.Font("wizard.bdf")
        pyxel.run(self.update, self.draw)

    def update(self):

        # Toggle between info mode
        if pyxel.btnp(pyxel.KEY_LALT, True, 1) and pyxel.btnp(pyxel.KEY_I):
            if self.progress != self.end:
                # dip if a response is still being displayed
                return

            self.info_mode = not self.info_mode

            if self.info_mode:
                self.input_text = INFO_INPUT
                self.output_text = INFO_OUTPUT
            else:
                self.input_text = ""
                self.output_text = " "
                self.partial_text = ""
            return

        # Do nothing if we're in info mode
        if self.info_mode:
            return

        # Clear the screen
        if pyxel.btnp(pyxel.KEY_LALT, True, 1) and pyxel.btnp(pyxel.KEY_C):
            self.input_text = ""
            self.output_text = " "
            return

        # Add a character to the input box - don't bother if we've passed the limit (tough if the question is too long)
        if len(self.input_text) < CHARACTER_LIMIT:
            self.input_text += _get_character()

        # Handle backspace to remove last character
        if pyxel.btnp(pyxel.KEY_BACKSPACE, True, 1) and self.input_text:
            self.input_text = self.input_text[:-1]

        # Generate a reply when the user hits Enter
        if pyxel.btnp(pyxel.KEY_RETURN) and self.input_text:
            traffic_count = get_traffic_count()
            self.output_text = ask_question(self.input_text, traffic_count)
            self.output_text = _split_up_long_text(self.output_text)
            print(self.output_text)
            self.end = len(self.output_text)
            self.progress = 1

    def draw(self):
        # Clear the screen
        pyxel.cls(7)

        # Fill with the background image
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
            PADDING - 1, OUTPUT_BOX_Y - 1, BOX_WIDTH + 2, OUTPUT_BOX_HEIGHT + 2, 8
        )  # Red border for output box
        pyxel.rect(
            PADDING, OUTPUT_BOX_Y, BOX_WIDTH, OUTPUT_BOX_HEIGHT, 0
        )  # Black rectangle for output box

        if self.info_mode:
            pyxel.text(
                PADDING + 2, INPUT_BOX_Y + 2, self.input_text, pyxel.frame_count % 15
            )  # Display the input text

            pyxel.text(
                PADDING + 2, OUTPUT_BOX_Y + 2, self.output_text, 7
            )  # Display user output text
        else:
            pyxel.text(
                PADDING + 2, INPUT_BOX_Y + 2, self.input_text, 7
            )  # Display the input text

            pyxel.text(
                PADDING + 2, OUTPUT_BOX_Y + 2, self.partial_text, 7
            )  # Display user output text

            # Display the partial output text
            self.partial_text = self.output_text[: self.progress]

            # Increase the counter for the output text display - unless we're already at the end
            if self.progress < self.end:
                self.progress += 1

        pyxel.rect(
            0, APP_HEIGHT - 11, APP_WIDTH, 12, 8
        )  # Red line for instructions footer
        pyxel.rect(
            0, APP_HEIGHT - 10, APP_WIDTH, 10, 0
        )  # Black rectangle for instructions footer
        pyxel.text(2, APP_HEIGHT - 8, INSTRUCTIONS, 8)


# Run the application
App()
