import os
import sys
from urllib import parse
from threading import Thread

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *

from infi.systray import SysTrayIcon
import requests

from Data.Config import Loader

class GUIMain(QMainWindow):
    def __init__(self, loader, main):
        self._loader = loader
        self.data = self._loader.data
        self.config = self._loader.config

        self.version = self.data.version

        self.name = self.data.window_name

        self.main = main

        self.load_icon()

        super().__init__()

        self.statusbar = self.statusBar()
        self.menubar = self.menuBar()
        self.browser = QWebEngineView()
        self.main_widget = QWidget()
        self.main_widget.setLayout(QVBoxLayout())
        self.setCentralWidget(self.main_widget)

        self.setWindowIcon(QIcon(self.icon))
        self.setWindowTitle(self.name)

        self.setGeometry(300, 300, 300, 100)
        self.setFixedSize(300, 100)

        self.load_menubar()
        self.load_widget_panels()

        self.change_dark_theme()

        self.show()

        if self.config.access_token in [None, '']:
            self.toggle_browser(True)
            self.browser_toggle.setChecked(True)
        else:
            self.toggle_browser(False)
            if self.config.autostart:
                self.start_overwatch()

    def start_overwatch(self):
        self.overwatch_toggle.setText("Stop Overwatch")
        self.overwatch_toggle.setChecked(True)
        print("Starting Overwatch")

        self.thread = Thread(target=self.main.start_overwatch, args = (self,))
        self.thread.daemon = True
        self.thread.start()

    def stop_overwatch(self):
        self.overwatch_toggle.setText("Start Overwatch")
        self.overwatch_toggle.setChecked(False)
        print("Stop Overwatch")

    def toggle_overwatch(self, b):
        if b.isChecked():
            self.start_overwatch()
        else:
            self.stop_overwatch()

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
            self.setFixedSize(1000, 500)
            self.platform_menu.hide()
            self.overwatch_toggle.hide()
            self.browser.show()
        else:
            self.setFixedSize(300, 100)
            self.platform_menu.show()
            self.overwatch_toggle.show()
            self.browser.hide()

    def change_dark_theme(self):
        print("Activate Dark Theme")

    def change_light_theme(self):
        print("Activate Light Theme")

    def update_platform(self, platform):
        self.config.platform = platform
        self.config.save()

    def on_browser_load(self):
        self.browser.page().runJavaScript(
            "window.location.href", self.get_oauth_token
        )

    def get_oauth_token(self, loc):
        if "OwlSectorAuth" in loc:
            params = {k: v[0] for k, v in parse.parse_qs(parse.urlsplit(loc).query).items()}

            headers = {
                "Content-Type": "application/x-www-form-urlencoded"
            }

            data = {
                "grant_type": "authorization_code",
                "code": params['code'],
                "client_id": 34375
            }

            r = requests.post("https://www.bungie.net/platform/app/oauth/token/", headers = headers, data=data)
            if r.status_code == 200:
                data = r.json()

                self.config.access_token = data.get('access_token')
                self.config.refresh_token = data.get('refresh_token')
                self.config.token_type = data.get('token_type')
                self.config.membership_id = data.get('membership_id')

                self.config.save()

                self.toggle_browser(False)

            else:
                data = {"error": r.status_code, "error_description": f"Token request failed with status code {r.status_code}"}

                error_box = QMessageBox.warning(f"ERROR:  {data['error_description']}.\n\nPlease try again.", QMessageBox.Ok, QMessageBox.Ok)

                if error_box == QMessageBox.Ok:
                    self.browser.setUrl(QUrl(self.data.oauth_url.format(client_id=self.data.client_id, state=self.config.state)))

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
        self.overwatch_widgets = QHBoxLayout()
        self.browser_widgets = QHBoxLayout()
        self.main_widget.layout().addLayout(self.overwatch_widgets)
        self.main_widget.layout().addLayout(self.browser_widgets)

        self.platform_menu = QComboBox()
        self.platform_menu.addItems(self.data.platforms)
        i = self.platform_menu.findText(self.config.platform, Qt.MatchFixedString)
        if i >= 0:
            self.platform_menu.setCurrentIndex(i)
        self.platform_menu.currentIndexChanged[str].connect(self.update_platform)
        self.platform_menu.setFixedSize(100, 25)
        self.overwatch_widgets.addWidget(self.platform_menu)

        self.overwatch_toggle = QPushButton()
        self.overwatch_toggle.setCheckable(True)
        if self.config.autostart:
            self.overwatch_toggle.toggle()
            self.overwatch_toggle.setText("Stop Overwatch")
        else:
            self.overwatch_toggle.setText("Start Overwatch")
        self.overwatch_toggle.clicked.connect(lambda: self.toggle_overwatch(self.overwatch_toggle))
        self.overwatch_toggle.setFixedSize(175, 25)
        self.overwatch_widgets.addWidget(self.overwatch_toggle)

        self.browser.setUrl(QUrl(self.data.oauth_url.format(client_id=self.data.client_id, state=self.config.state)))
        self.browser.loadFinished.connect(self.on_browser_load)
        self.browser_widgets.addWidget(self.browser)
