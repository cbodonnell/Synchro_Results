import tkinter
from tkinter import filedialog
import os

def browse_for_path():
    #Sets up GUI
    root = tkinter.Tk()
    root.withdraw()
    root.lift()
    root.update()
    currdir = os.getcwd()
    fileName = filedialog.askopenfilename(initialdir=currdir, title='Please select the Synchro report').replace('//', '/').replace('/','//')
    root.destroy()
    root.quit()
    return fileName
