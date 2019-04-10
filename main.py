# encoding: utf-8

# System
import os
import configparser

# Global
from libs.OpenGL.camera import Camera
from settings import Settings
from libs.library import Library
from libs.Qt.vwindow import *
from libs.Qt.vapplication import *

# Global - Library
from libs.OpenGL.DataLoader.dataloader import *
from PyQt5.QtWidgets import QApplication

try:
   from OpenGL.GL import *
except Exception as e:
   print("Exception :: {0}".format(str(e)))

def main():
   workingDir_s = os.getcwd()
   readInits(workingDir_s, "game.ini")
   initLibraries()

   start_scr = Settings.gameSettings["scriptstart"]["path"]
   # Execute first scripts
   try:
      # read file
      fullExecPath = os.path.join(workingDir_s, Settings.engineDir, start_scr, "view" + ".py")
      if os.path.isfile(fullExecPath):
         exec(open(fullExecPath).read(), globals())
   except Exception as ex:
      print("Exception :: {0}".format(str(ex)))

   sys.exit(Library.app.exec_())



def iniToDict(dir_s, filename_s):
   retDict_o = dict()
   try:
      parser = configparser.ConfigParser()
      completePath_s = os.path.join(dir_s, filename_s)
      if os.path.isfile(completePath_s):
         parser.read(completePath_s,"utf-8")
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
      # Important - Window basics
      Library.app = QApplication(sys.argv)
      Library.mainWindow = VWindow(50, 50, 1200, 1200, None)
      Library.mainWindow.show()
      # OpenGL - DB Loading
      Library.loader = DataLoader()
      Library.camera = Camera()

   except Exception as ex:
      print("Exception :: {0}".format(str(ex)))


if __name__ == "__main__":
   main()