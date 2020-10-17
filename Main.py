import asyncio
import os
import json
import sys
import time
import traceback
from urllib import parse

from PyQt5.QtWidgets import *
from DestinyManifestManager import Manifest
import requests
from pypresence import Presence

from GUIMain import GUIMain
from Enums.Platforms import Platforms
from Enums.Errors import Errors
from Data.Config import Loader

BASE_ROUTE = "https://www.bungie.net/Platform"
ACTIVITY_LOOKUP = BASE_ROUTE + "/Destiny2/{0}/Profile/{1}/Character/{2}/?components=CharacterActivities"
CHARACTER_LOOKUP = BASE_ROUTE + "/Destiny2/{0}/Profile/{1}/?components=Characters"
MEMBERSHIP_ID_LOOKUP = BASE_ROUTE + "/Destiny2/SearchDestinyPlayer/{0}/{1}"

class Requests:
    def __init__(self, config, errors):
        self.errors = errors

        self.access_token = config.access_token
        self.headers = {"X-API-Key": self.access_token}

    def get(self, request):
        self.data = requests.get(parse.quote(request, safe=':/?&=,.'), headers = self.headers).json()

        if self.data.get("Response", False) == False:
            print(request + ":")
            print(json.dumps(self.data, indent = 4))

        if self.data.get("ErrorCode", False) == 2101:
            return self.errors.error("invalid_token")
        if self.data.get("ErrorCode", False) == 5:
            return self.errors.error("server_not_found")

        return self.data

class Main:
    def __init__(self, loader, manifest):
        self._loader = loader
        self.data = self._loader.data
        self.config = self._loader.config
        self.manifest = manifest

        self.run = True
        self.language = self.config.language

    def start_overwatch(self, gui):
        RPC = Presence('767085094875168778', loop = asyncio.new_event_loop())
        RPC.connect()

        platform = Platforms(self.config.platform)

        requester = Requests(self.config, Errors())

        while True:
            try:
                if not self.run:
                    RPC.close()
                    return

                last_player_char = self.get_last_played_id(platform.platform, self.config.membership_id, requester)

                time.sleep(30)

                self.run = False
            except Exception as e:
                print(traceback.format_exc())

    def get_last_played_id(self, type, id, requester):
        character_data = requests.get(CHARACTER_LOOKUP.format(type, id))

        epoch_table = {}

        for k, v in character_data["Response"]["characters"]["data"].items():
            epoch_table[self.date_to_epoch(v["dateLastPlayed"])] = key

        return epoch_table[max(epoch_character_table.keys())]

    def date_to_epoch(self, date):
        epoch = datetime.datetime.(1970, 1, 1)
        dt = datetime.datetime.strptime(date.replace("T", " ").replace("Z", ""), "%Y-%m-%d %H:%M:%S")
        epoch_diff = (dt - epoch).total_seconds()
        return epoch_diff

if __name__ == "__main__":
    mani = Manifest(loc = 'Manifest')

    loader = Loader()

    main = Main(loader, mani)

    app = QApplication(sys.argv)
    gui = GUIMain(loader, main)
    sys.exit(app.exec_())
