# encoding: utf-8
import os
from OpenGL.GL import *

from .textureloader import loadTexture

class Texture:
   TEX_PATH = "data/res"
   def __init__(self, filename, unit):
      fullPath = os.path.join(Texture.TEX_PATH, filename)
      if os.path.isfile(fullPath):
         self.filename = filename
         if self.filename == "characterTexture.png" or self.filename == "mud.png":
            self.vbo = loadTexture(fullPath, GL_RGBA)
         else:
            self.vbo = loadTexture(fullPath, GL_RGB)

         self.unit = unit
      else:
         raise Exception("File not found {}".format(fullPath))

