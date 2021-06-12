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
            glGenerateMipmap(GL_TEXTURE_2D)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_LOD_BIAS, -0.4)
            if fullPath.endswith(".png"):
                self.vbo = loadTexture(fullPath, GL_RGBA)
            else:
                self.vbo = loadTexture(fullPath, GL_RGB) # TODO: Corrent readings
            self.unit = unit
        else:
            raise Exception("__init__: texture [ERROR] File not found {}".format(fullPath))
