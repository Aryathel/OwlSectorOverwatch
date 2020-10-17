import os
import sys
from tkinter import Frame

from infi.systray import SysTrayIcon

from Data.Config import Loader

class GUIMain(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)

        self._loader = Loader()
        self.data = self._loader.data
        self.config = self._loader.config

        self.version = self.data.version

        self.name = self.data.window_name
        self.master.title(self.name)

        self.load_icon()
        self.tray()

    def tray(self):
        tray = (("Open Window", None, self.open_window), ("Start", None, self.start_overwatch), ("Stop", None, self.stop_overwatch))
        self.systray = SysTrayIcon(self.icon, self.name, tray, on_quit=self.quit_program)
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

    def load_icon(self):
        fileName = f"./{self.data.directory_name}/Resources/Owl_Sector.ico"
        if not os.path.isfile(fileName):
            with open(fileName, "w+") as file:
                icon = requests.get(self.config.icon_url)
                file.write(icon.content)

        return fileName
