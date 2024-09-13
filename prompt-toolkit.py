from prompt_toolkit import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout

buffer1 = Buffer()  # Editable buffer.

root_container = HSplit([
    # One window that holds the BufferControl with the default buffer on
    # the left.
    

    # A vertical line in the middle. We explicitly specify the width, to
    # make sure that the layout engine will not try to divide the whole
    # width by three for all these windows. The window will simply fill its
    Window(content=FormattedTextControl(text='Hello world')),
    # content by repeating this character.
    Window(width=1, char='-'),

    # Display the text 'Hello world' on the right.
    
    Window(content=BufferControl(buffer=buffer1)),
])

layout = Layout(root_container)

app = Application(layout=layout, full_screen=True)
app.run() # You won't be able to Exit this app