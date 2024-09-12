import sys, os
sys.path.append(os.path.join(sys.path[0],'../../..'))

import TermTk as ttk

# layout = GridLayout
#   It is required to allow the tabWidget to be automatically resized to the "root" area
# mouseTrack = True (optional)
#   It is required if we want to forward the mouse over events to the terminals
#   i.e. the mouse over feature of pytermTk or Textual
root = ttk.TTk(layout=ttk.TTkGridLayout(), mouseTrack=True)

tab = ttk.TTkTabWidget(parent=root)

menu = tab.addMenu("Add Terminal")

def _addTerminal():
    num = tab.count() + 1
    term = ttk.TTkTerminal()
    th = ttk.TTkTerminalHelper(term=term)
    tab.addTab(term, f"Terminal {num}")
    tab.setCurrentWidget(term)
    th.runShell()

menu.menuButtonClicked.connect(_addTerminal)

root.mainloop()