import json
import os

import requests

class Data:
    def __init__(self, options):
        self.window_name = options.get('window_name')
        self.version = options.get('version')
        self.icon_url = options.get('icon_url')
        self.directory_name = options.get('directory_name')
        self.platforms = options.get('platforms')
        self.version_url = options.get('version_url')
        self.locales = options.get("supported_locales")

class Config:
    def __init__(self, options):
        self.api_token = options.get('api_token')
        self.platform = options.get('platform')
        self.username = options.get('username')
        self.language = options.get('language')
        self.autostart = options.get('autostart')
        self.id_search = options.get('id_search')

class Loader:
    def __init__(self):
        self.repo_url = "https://raw.githubusercontent.com/HeroicosHM/OwlSectorOverwatch"
        self.data_url = f"{self.repo_url}/master/OwlSector.json"

        self._load_data()
        self._load_config()

    def _load_data(self):
        data = requests.get(self.data_url).json()
        seelf.data = Data(data)

    def _load_config(self):
        if os.path.isfile(f"./{self.data.directory_name}/config.json"):
            with open(f"./{self.data.directory_name}/config.json", "r") as file:
                self.config = Config(json.load(file))
        else:
            with open(f"./{self.data.directory_name}/config.json", "w+") as file:
                self.config = Config({
                    "api_token": "",
                    "platform": self.data.platforms[0],
                    "username": "",
                    "language": self.data.locales[0],
                    "autostart": False,
                    "id_search": False
                })
                self.config.save(file)
