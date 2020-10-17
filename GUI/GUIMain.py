import sys
from tkinter import Frame

from infi.systray import SysTrayIcon

from Data.Config import Config

class GUIMain(Frame):
    def __init__(self, root, resourceDir = "./Resources", name = "Owl Sector Overwatch", data = {}):
        Frame.__init__(self, root)
        self.version = "0.0.1"
        self.resources = resourceDir
        self.name = name
        self.master.title(self.name)

        self.data = data

        self.config = Config().data

        tray = (("Open Window", None, self.open_window), ("Start", None, self.start_overwatch), ("Stop", None, self.stop_overwatch))
        self.systray = SysTrayIcon(f"{self.resources}/Owl_Sector.ico", self.name, tray, on_quit=self.quit_program)
        self.systray.start()
        self.master.protocol("WM_DELETE_WINDOW", self.vanish)

    def open_window(self, e=None):
        self.master.update()
        self.master.deiconify()

    def start_overwatch(self, e=None):
        print("Start Overwatch")

    def stop_overwatch(self, e=None):
        print("Stop Overwatch")

    def quit_program(self, e=None):
        sys.exit(0)

    def vanish(self):
        self.master.withdraw()
