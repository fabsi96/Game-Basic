# encoding: utf-8
import os

from OpenGL.GL import *
import numpy as np
from PIL import Image
import pygame
import cv2
from glm import tmat4x4

from libs.OpenGL.DAL.Outer.vobject import VOpenGL
from libs.OpenGL.DataLoader.Texture.texture import Texture
from libs.library import Library


class VCubeMap(VOpenGL):
   SIZE = 100
   VERTICES = [
       -SIZE,  SIZE, -SIZE,
	    -SIZE, -SIZE, -SIZE,
	     SIZE, -SIZE, -SIZE,
	     SIZE, -SIZE, -SIZE,
	     SIZE,  SIZE, -SIZE,
	    -SIZE,  SIZE, -SIZE,

	    -SIZE, -SIZE,  SIZE,
	    -SIZE, -SIZE, -SIZE,
	    -SIZE,  SIZE, -SIZE,
	    -SIZE,  SIZE, -SIZE,
	    -SIZE,  SIZE,  SIZE,
	    -SIZE, -SIZE,  SIZE,

	     SIZE, -SIZE, -SIZE,
	     SIZE, -SIZE,  SIZE,
	     SIZE,  SIZE,  SIZE,
	     SIZE,  SIZE,  SIZE,
	     SIZE,  SIZE, -SIZE,
	     SIZE, -SIZE, -SIZE,

	    -SIZE, -SIZE,  SIZE,
	    -SIZE,  SIZE,  SIZE,
	     SIZE,  SIZE,  SIZE,
	     SIZE,  SIZE,  SIZE,
	     SIZE, -SIZE,  SIZE,
	    -SIZE, -SIZE,  SIZE,

	    -SIZE,  SIZE, -SIZE,
	     SIZE,  SIZE, -SIZE,
	     SIZE,  SIZE,  SIZE,
	     SIZE,  SIZE,  SIZE,
	    -SIZE,  SIZE,  SIZE,
	    -SIZE,  SIZE, -SIZE,

	    -SIZE, -SIZE, -SIZE,
	    -SIZE, -SIZE,  SIZE,
	     SIZE, -SIZE, -SIZE,
	     SIZE, -SIZE, -SIZE,
	    -SIZE, -SIZE,  SIZE,
	     SIZE, -SIZE,  SIZE]

   def __init__(self, rawObject, shaderProg):
      try:
         rawObject.vertexCoords = VCubeMap.VERTICES
         rawObject.normalCoords = []
         rawObject.textureCoords = []
         rawObject.textureFiles = []
         rawObject.renderMode = "ARRAYS"
         # Correct order! Right - Left - Top - Bottom - Back - Front
         rawObject.textureFiles.append("right.png")
         rawObject.textureFiles.append("left.png")
         rawObject.textureFiles.append("top.png")
         rawObject.textureFiles.append("bottom.png")
         rawObject.textureFiles.append("back.png")
         rawObject.textureFiles.append("front.png")
         super(VCubeMap, self).__init__(rawObject, shaderProg)
         self.sp.loadMatrix4x4("projectionMatrix")
         self.sp.loadMatrix4x4("viewMatrix")

         self.__uploadCubeMap("sky", rawObject.textureFiles)

      except Exception as ex:
         print(str(ex))

   def __uploadCubeMap(self, cubeMapFolder, filesOrder):
      # Upload cubemap textures
      self.sp.start()
      self.cubeTexID = glGenTextures(1)
      glActiveTexture(GL_TEXTURE0)
      glBindTexture(GL_TEXTURE_CUBE_MAP, self.cubeTexID)
      for i in range(0, 6):
         fullPath = os.path.join("data/res", cubeMapFolder, filesOrder[i])
         image_rgb = Image.open(fullPath)
         image_rgba = image_rgb.convert("RGBA")
         img_data = np.array(image_rgba.getdata())
         glTexImage2D(GL_TEXTURE_CUBE_MAP_POSITIVE_X + i, 0, GL_RGBA, image_rgba.width, image_rgba.height, 0, GL_RGBA,
                      GL_UNSIGNED_BYTE, img_data)
      glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
      glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
      glTexParameteri(GL_TEXTURE_CUBE_MAP,GL_TEXTURE_WRAP_S,GL_CLAMP_TO_EDGE)
      glTexParameteri(GL_TEXTURE_CUBE_MAP,GL_TEXTURE_WRAP_T,GL_CLAMP_TO_EDGE)
      glTexParameteri(GL_TEXTURE_CUBE_MAP,GL_TEXTURE_WRAP_R,GL_CLAMP_TO_EDGE)
      self.sp.stop()

   def render(self):
      self.sp.start()
      glBindVertexArray(self.vao)
      glBindBuffer(GL_ARRAY_BUFFER, self.vertexVbo)

      self.sp.setMatrix4x4("projectionMatrix", Library.mainWindow.getProjectionMatrix())
      viewMatrix: tmat4x4 = Library.camera.getWorldToViewMatrix()
      self.sp.setMatrix4x4("viewMatrix", viewMatrix)
      glActiveTexture(GL_TEXTURE0)
      glBindTexture(GL_TEXTURE_CUBE_MAP, self.cubeTexID)
      glDrawArrays(GL_TRIANGLES, 0, self.vertexCount)

      glBindVertexArray(0)
      self.sp.stop()

