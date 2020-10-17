import os
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
import sys

from infi.systray import SysTrayIcon
import requests

from Data.Config import Loader

class GUIMain(QMainWindow):
    def __init__(self, loader):
        self._loader = loader
        self.data = self._loader.data
        self.config = self._loader.config

        self.version = self.data.version

        self.name = self.data.window_name

        self.load_icon()

        super().__init__()

        self.statusbar = self.statusBar()
        self.menubar = self.menuBar()
        self.browser = QWebEngineView()
        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)

        self.setWindowIcon(QIcon(self.icon))
        self.setWindowTitle(self.name)

        self.setGeometry(300, 300, 600, 200)

        self.load_menubar()
        self.load_widget_panels()

        self.change_dark_theme()

        self.show()

        self.statusbar.showMessage("Ready")

        if self.config.autostart:
            self.start_overwatch()

    def tray(self):
        tray = (("Open Window", None, self.open_window), ("Start", None, self.start_overwatch), ("Stop", None, self.stop_overwatch))
        self.systray = SysTrayIcon(self.icon, self.name, tray, on_quit=self.quit_program)
        self.systray.start()

    def open_window(self, e=None):
        pass

    def start_overwatch(self):
        self.overwatch_toggle.setText("Stop Overwatch")
        self.overwatch_toggle.setChecked(True)
        print("Start Overwatch")

    def stop_overwatch(self):
        self.overwatch_toggle.setText("Start Overwatch")
        self.overwatch_toggle.setChecked(False)
        print("Stop Overwatch")

    def toggle_overwatch(self, b):
        if b.isChecked():
            self.start_overwatch()
        else:
            self.stop_overwatch()

    def quit_program(self):
        sys.exit(0)

    def vanish(self):
        pass

    def load_icon(self):
        fileName = f"./{self.data.directory_name}/Resources/Owl_Sector.png"
        if not os.path.isdir(f"./{self.data.directory_name}/Resources/"):
            os.mkdir(f"./{self.data.directory_name}/Resources/")

        if not os.path.isfile(fileName):
            with open(fileName, "wb+") as file:
                icon = requests.get(self.data.icon_url)
                file.write(icon.content)

        self.icon = fileName

    def toggle_auto_start(self, state):
        self.config.autostart = state
        self.config.save()

    def toggle_id_search(self, state):
        self.config.id_search = state
        self.config.save()

    def toggle_browser(self, state):
        if state:
            self.browser.show()
        else:
            self.browser.hide()

    def change_dark_theme(self):
        print("Activate Dark Theme")

    def change_light_theme(self):
        print("Activate Light Theme")

    def update_platform(self, platform):
        self.config.platform = platform
        self.config.save()

    def load_menubar(self):
        self.exit = QAction('&Exit', self)
        self.exit.setShortcut('Ctrl+Q')
        self.exit.setStatusTip('Quit Program')
        self.exit.triggered.connect(qApp.quit)

        self.start = QAction('Start', self)
        self.start.setStatusTip('Start Overwatch')
        self.start.triggered.connect(self.start_overwatch)

        self.stop = QAction('Stop', self)
        self.stop.setStatusTip('Stop Overwatch')
        self.stop.triggered.connect(self.stop_overwatch)

        self.autostart = QAction('Autostart', self, checkable = True)
        self.autostart.setStatusTip('Start Overwatch automatically on program launch.')
        self.autostart.setChecked(self.config.autostart)
        self.autostart.triggered.connect(self.toggle_auto_start)

        self.dark_theme = QAction('Dark Theme', self)
        self.dark_theme.setStatusTip('Change to dark theme.')
        self.dark_theme.triggered.connect(self.change_dark_theme)

        self.light_theme = QAction('Light Theme', self)
        self.light_theme.setStatusTip('Change to light theme.')
        self.light_theme.triggered.connect(self.change_light_theme)

        self.browser_toggle = QAction('Show Browser', self, checkable = True)
        self.browser_toggle.setStatusTip('Shows the browser page.')
        self.browser_toggle.setChecked(False)
        self.browser_toggle.triggered.connect(self.toggle_browser)

        self.menu_owl_sector = self.menubar.addMenu('&Owl Sector')

        self.menu_owl_sector.addAction(self.start)
        self.menu_owl_sector.addAction(self.stop)
        self.menu_owl_sector.addAction(self.autostart)
        self.menu_owl_sector.addAction(self.exit)

        self.menu_themes = self.menubar.addMenu('&Themes')

        self.menu_themes.addAction(self.dark_theme)
        self.menu_themes.addAction(self.light_theme)

        self.menu_links = self.menubar.addMenu('&Links')

        self.menu_links.addAction(self.browser_toggle)

    def load_widget_panels(self):
        self.layout = QVBoxLayout()

        self.platform_menu = QComboBox()
        self.platform_menu.addItems(self.data.platforms)
        i = self.platform_menu.findText(self.config.platform, Qt.MatchFixedString)
        if i >= 0:
            self.platform_menu.setCurrentIndex(i)
        self.platform_menu.currentIndexChanged[str].connect(self.update_platform)
        self.layout.addWidget(self.platform_menu)

        self.overwatch_toggle = QPushButton()
        self.overwatch_toggle.setCheckable(True)
        if self.config.autostart:
            self.overwatch_toggle.toggle()
            self.overwatch_toggle.setText("Stop Overwatch")
        else:
            self.overwatch_toggle.setText("Start Overwatch")
        self.overwatch_toggle.clicked.connect(lambda: self.toggle_overwatch(self.overwatch_toggle))
        self.layout.addWidget(self.overwatch_toggle)

        self.browser.setUrl(QUrl(self.data.oauth_url.format(client_id=self.data.client_id, state=self.config.state)))
        self.layout.addWidget(self.browser)
        self.browser.hide()

        self.widget.setLayout(self.layout)
