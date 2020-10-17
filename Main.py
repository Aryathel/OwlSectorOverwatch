import os
import time
from tkinter import Tk

from DestinyManifestManager import Manifest

from GUI.GUIMain import GUIMain

BASE_ROUTE = "https://www.bungie.net/Platform"
ACTIVITY_LOOKUP = BASE_ROUTE + "/Destiny2/{0}/Profile/{1}/Character/{2}/?components=CharacterActivities"
CHARACTER_LOOKUP = BASE_ROUTE + "/Destiny2/{0}/Profile/{1}/?components=Characters"
MEMBERSHIP_ID_LOOKUP = BASE_ROUTE + "/Destiny2/SearchDestinyPlayer/{0}/{1}"

if __name__ == "__main__":
    root = Tk()

    mani = Manifest(loc = 'Manifest')
    mani.update_manifest('en')

    GUIMain(root)

    time.sleep(50000)
