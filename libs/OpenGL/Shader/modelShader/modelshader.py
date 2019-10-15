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
      except Exception as ex:
         print(str(ex))

