import pyxel

APP_WIDTH = 256 * 2
APP_HEIGHT = 144 * 2


class App:
    def __init__(self):
        pyxel.init(APP_WIDTH, APP_HEIGHT, title="Simple UI")
        self.input_text = ""
        self.output_text = ""
        self.is_typing = True  # Track if typing in input box
        pyxel.mouse(True)  # Enable mouse
        pyxel.run(self.update, self.draw)

    def update(self):
        # Handle typing in the input box
        if self.is_typing:
            for i in range(pyxel.KEY_A, pyxel.KEY_Z + 1):
                if pyxel.btnp(i):
                    self.input_text += chr(i + 32)  # Convert key to lowercase

            if pyxel.btnp(pyxel.KEY_BACKSPACE) and self.input_text:
                self.input_text = self.input_text[:-1]

            if pyxel.btnp(pyxel.KEY_SPACE):
                self.input_text += " "

        # Check for submit button click
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            if 100 <= pyxel.mouse_x <= 140 and 50 <= pyxel.mouse_y <= 60:
                self.output_text = f"You entered: {self.input_text}"
                self.input_text = ""  # Clear input after submission

    def draw(self):
        pyxel.cls(7)  # Clear screen to white

        # Draw instruction text at the top
        pyxel.text(10, 10, "Type in your query:", 0)

        # Draw input box
        pyxel.rect(10, 50, 90, 10, 0)  # Black rectangle for input box
        pyxel.text(12, 52, self.input_text, 7)  # Display user input text

        # Draw submit button
        pyxel.rect(100, 50, 40, 10, 8)  # Red rectangle for button
        pyxel.text(105, 52, "Submit", 7)  # Submit button label

        # Draw output box
        pyxel.rect(10, 80, 130, 20, 0)  # Black rectangle for output box
        pyxel.text(12, 85, self.output_text, 7)  # Display the output text


# Run the application
App()
