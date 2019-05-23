from tkinter import*
from tkinter import font
from mainFrame import*
from resultFrame import*

CITY=0
DISTRICT=1
TOWN=2

class framework:
    window=None
    mFrame=None
    rFrame=None
    def __init__(self):
        framework.window = Tk()

        framework.mFrame=mainFrame.Frame()

        framework.window.mainloop()
    def select(self):
        pass




Framework = framework()