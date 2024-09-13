import time
from threading import Thread
import pytermgui as ptg


# Function to simulate processing and generate a response
def process_input(input_text):
    # Simulate a long-running process
    time.sleep(3)  # Replace with actual processing code
    return f"Response to '{input_text}'"



def main():

    # Create the layout
    with ptg.WindowManager() as manager:
        manager.layout.add_slot("Body")
        # Create the main window

        input_box = ptg.InputField()
        response_text = ptg.Label("")

        def on_submit():
            # Disable input box and show ellipses
            input_box.disabled = True
            response_text.text = "Processing..."
            response_text.text = process_input(input_box.value)
            input_box.disabled = False

        window = ptg.Window(
            ptg.Label("Type in your query and press SUBMIT:", box="EMPTY"),
            ptg.Container(
                input_box, box="SINGLE"
            ),
            ptg.Button("Submit", on_click= lambda _: on_submit()),
            response_text,  # To display the response or ellipses
        )

        # Add widgets to the window
        manager.add(window)


if __name__ == "__main__":
    main()
