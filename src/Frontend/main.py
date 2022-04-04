# encoding: utf-8

# System
from src.start.view import StartView
from core.graphics.dataloader.dataloader import DataLoader
from core.graphics.camera import Camera
from core.gui.vglwidget import VGLWidget
from core.library import Library
from settings import Settings

try:
    import sys
    import os
    import configparser
    import time
    from threading import *
except Exception as e:
    print("Exception :: {0}".format(str(e)))

# Global
try:
    from PyQt5.QtWidgets import QApplication

except Exception as e:
    print("Exception :: {0}".format(str(e)))

try:
    from OpenGL.GL import *
except Exception as e:
    print("Exception :: {0}".format(str(e)))


def main():
    workingDir_s = os.getcwd()
    readInits(workingDir_s, "game.ini")
    initLibraries()

    sys.exit(Library.app.exec())

def iniToDict(dir_s, filename_s):
    retDict_o = dict()
    try:
        parser = configparser.ConfigParser()
        completePath_s = os.path.join(dir_s, filename_s)
        if os.path.isfile(completePath_s):
            parser.read(completePath_s, "utf-8")
            retDict_o = parser.__dict__

    except Exception as ex:
        print("Exception {0}".format(str(ex)))

    return retDict_o

def readInits(workingDir_s, game_s, server_s="", data_s=""):
    try:
        gameConfigs_o = iniToDict(workingDir_s, game_s)
        settings_o = gameConfigs_o["_sections"]
        Settings.gameSettings["window"] = settings_o["window"]
        Settings.gameSettings["scriptstart"] = settings_o["scriptstart"]
        Settings.dataSettings = settings_o["data"]
    except Exception as ex:
        print("Exception :: {0}".format(str(ex)))

def initLibraries():
    try:
        Library.app = QApplication(sys.argv)
        # graphics - DB Loading
        Library.loader = DataLoader()
        Library.camera = Camera()

        # Important - Window basics
        windowWidth_i = int(Settings.gameSettings["window"]["width"])
        windowHeight_i = int(Settings.gameSettings["window"]["height"])
        Library.mainWindow = VGLWidget(1000, 1000)
        Library.mainWindow.show()

    except Exception as ex:
        print("Exception :: {0}".format(str(ex)))

if __name__ == "__main__":
    main()
