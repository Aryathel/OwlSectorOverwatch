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
        self.client_id = options.get("client_id")
        self.oauth_url = options.get("oauth_url")

class Config:
    def __init__(self, options, file):
        self.access_token = options.get('access_token')
        self.refresh_token = options.get('refresh_token')
        self.token_type = options.get('token_type')
        self.membership_id = options.get('membership_id')
        self.platform = options.get('platform', 'Steam')
        self.username = options.get('username')
        self.language = options.get('language', 'en')
        self.autostart = options.get('autostart', False)
        self.state = options.get('state')

        self.file = file

    def save(self):
        with open(self.file, "w+") as confFile:
            json.dump(self.__dict__, confFile, indent = 4, sort_keys = True)

class Loader:
    def __init__(self):
        self.repo_url = "https://raw.githubusercontent.com/HeroicosHM/OwlSectorOverwatch"
        self.data_url = f"{self.repo_url}/master/OwlSector.json"

        self._load_data()
        self._load_config()

    def _load_data(self):
        data = requests.get(self.data_url).json()
        self.data = Data(data)

    def _load_config(self):
        if not os.path.isdir(f"./{self.data.directory_name}/"):
            os.mkdir(f"./{self.data.directory_name}/")

        if os.path.isfile(f"./{self.data.directory_name}/config.json"):
            with open(f"./{self.data.directory_name}/config.json", "r") as file:
                self.config = Config(json.load(file), f"./{self.data.directory_name}/config.json")
        else:
            self.config = Config({
                "acess_token": "",
                "refresh_token": "",
                "token_type": "",
                "membership_id": 0,
                "platform": self.data.platforms[0],
                "username": "",
                "language": self.data.locales[0],
                "autostart": False
            },
            f"./{self.data.directory_name}/config.json")
            self.config.save()
