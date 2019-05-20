# encoding: utf-8
from libs.library import Library

try:
   from OpenGL.GL import *
   from glm.gtc.matrix_transform import *
   import numpy as np

   from libs.OpenGL.Shader.shaderloader import getShader
   from libs.OpenGL.Shader.shaderprogram import ShaderProgram
   from libs.Qt.vwindow import VGLWindow
except Exception as e:
   print("Import Exception :: {}".format(str(e)))

class ModelShader(ShaderProgram):
   def __init__(self):
      try:
         super(ModelShader, self).__init__("ModelShader", getShader("libs/OpenGL/Shader/ModelShader", "modelShader", "modelShader", VGLWindow.ShaderVersion))

         # Ambient light (basic groundcolor)
         self.__ambientLightColor = tvec3([.1, .1, 0.1])
         self.__ambientLightShaderName = "ambientLight"

         # Diffuse light (specific, light positioned and object positioned dependend)
         self.__diffuseLightPosition = tvec3([0.0, 0.0, 0.0])
         self.__diffuseLightPositionShaderName = "lightPosition"

         self.makeAmbientLight()
         self.makeDiffuseLight()
         # self.makeSpecularLight()

      except Exception as ex:
         print(str(ex))

   def start(self):
      try:
         super(ModelShader, self).start()
         # self.updateSpecularLight()

      except Exception as ex:
         raise ex

   def makeAmbientLight(self):
      """ Ambient light """
      try:
         self.start()
         self.loadVector3f(self.__ambientLightShaderName)
         self.setVector3f(self.__ambientLightShaderName, np.array(self.__ambientLightColor, dtype=np.float32))
         self.stop()

      except Exception as ex:
         print("shader ex :: {}".format(str(ex)))

   def setAmbientLightColor(self, color: tvec3):
      self.__ambientLightColor = color

   def makeDiffuseLight(self):
      """ Diffuse light """
      try:
         self.start()
         # Light position
         self.loadVector3f(self.__diffuseLightPositionShaderName)
         self.setVector3f(self.__diffuseLightPositionShaderName, np.array(self.__diffuseLightPosition, dtype=np.float32))
         self.stop()

      except Exception as ex:
         print("{}".format(str(ex)))

   # TODO
   # SUM of lights to be addable
   def setLightPosition(self, newPosition: tvec3):
      try:
         self.__diffuseLightPosition = np.array(newPosition, dtype=np.float32)
         self.start()
         self.setVector3f(self.__diffuseLightPositionShaderName, self.__diffuseLightPosition)
         self.stop()

      except Exception as ex:
         raise ex

   def getLightPosition(self):
      return self.__diffuseLightPosition

   def makeSpecularLight(self):
      try:
         self.start()
         self.loadVector3f("cameraPosition")
         self.setVector3f("cameraPosition", np.array(Library.camera.getPosition(), dtype=GLfloat))
         self.stop()

      except Exception as ex:
         raise ex

   def updateSpecularLight(self):
      try:
         if Library.camera is not None:
            self.loadVector3f("cameraPosition")
            self.setVector3f("cameraPosition", np.array(Library.camera.getPosition(), dtype=GLfloat))

      except Exception as ex:
         raise ex