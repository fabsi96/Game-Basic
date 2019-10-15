# encoding: utf-8
import numpy

from OpenGL.GL import *
from PIL import Image


def loadTexture(fullPath, COLOR_MODE):
   try:
      # Texture
      texturevbo = glGenTextures(1)
      glBindTexture(GL_TEXTURE_2D, texturevbo)
      # Set the texture wrapping parameters
      glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
      glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
      # Set texture filtering parameters
      glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
      glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)


      """
         Load image-data into gpu cache
         TODO: diffrent image-data settings
      """
      image = Image.open(fullPath)# .transpose(Image.FLIP_TOP_BOTTOM)
      img_data = numpy.array(list(image.getdata()), numpy.uint8)
      glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height, 0, COLOR_MODE, GL_UNSIGNED_BYTE, img_data)

      glEnable(GL_TEXTURE_2D)
   except Exception as ex:
      raise ex

   return texturevbo