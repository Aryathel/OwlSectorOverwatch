import os
import sys
import time

from PyQt5.QtWidgets import *
from DestinyManifestManager import Manifest

from GUI.GUIMain import GUIMain
from Data.Config import Loader

BASE_ROUTE = "https://www.bungie.net/Platform"
ACTIVITY_LOOKUP = BASE_ROUTE + "/Destiny2/{0}/Profile/{1}/Character/{2}/?components=CharacterActivities"
CHARACTER_LOOKUP = BASE_ROUTE + "/Destiny2/{0}/Profile/{1}/?components=Characters"
MEMBERSHIP_ID_LOOKUP = BASE_ROUTE + "/Destiny2/SearchDestinyPlayer/{0}/{1}"

if __name__ == "__main__":
    mani = Manifest(loc = 'Manifest')
    #mani.update_manifest('en')

    loader = Loader()

    app = QApplication(sys.argv)
    gui = GUIMain(loader)
    sys.exit(app.exec_())
