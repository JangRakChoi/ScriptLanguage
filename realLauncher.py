from tkinter import*
from tkinter import font
import mainFrame
CITY = 0
DISTRICT = 1
TOWN = 2

mFrame=None
rFrame=None

def SetMainFrame():
    global mFrame
    mFrame = mainFrame.Frame()

class Window():
    window=Tk()
    window.mainloop()
