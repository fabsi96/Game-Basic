# encoding: utf-8
from PyQt5.QtWidgets import QApplication


class Library:
   TEXTURE_PATH = "data"
   loader  = None
   app: QApplication = None
   mainWindow  = None
   camera = None
   libs = {""}

   # Map
   vMap = None

