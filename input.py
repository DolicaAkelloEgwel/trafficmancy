import time
from threading import Thread
import pytermgui as ptg


# Function to simulate processing and generate a response
def process_input(input_text, callback):
    # Simulate a long-running process
    time.sleep(3)  # Replace with actual processing code
    response = f"Response to '{input_text}'"
    callback(response)


def on_submit():
    pass


def main():

    # Create the layout
    with ptg.WindowManager() as manager:
        manager.layout.add_slot("Body")
        # Create the main window

        window = ptg.Window(
            ptg.Label("Type in your query and press SUBMIT:", box="EMPTY"),
            ptg.Container(
                ptg.InputField(placeholder="Enter your query here..."), box="SINGLE"
            ),
            ptg.Button("Submit", on_click=on_submit),
            ptg.Window("", box="EMPTY"),  # To display the response or ellipses
        )

        # Add widgets to the window
        manager.add(window)


if __name__ == "__main__":
    main()
