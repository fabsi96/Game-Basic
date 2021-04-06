# encoding: utf-8
from libs.Qt.vglwidget import VGLWidget

try:
   import os
except Exception as e:
   print(f"Import exception {str(e)}")

try:
   from libs.OpenGL.Shader.shaderloader import getShader
   from libs.OpenGL.Shader.shaderprogram import ShaderProgram
except Exception as e:
   print(f"Import exception {str(e)}")

# -----------------
class MapShader (ShaderProgram):
# -----------------
   """ Summary
   """
   MAP_DIR = "MapShader"
   # -----------------
   def __init__(self):
   # -----------------
      try:
         super(MapShader, self).__init__(self.MAP_DIR, getShader(os.path.join(ShaderProgram.SHADER_DIR, self.MAP_DIR), self.MAP_DIR,
                                                                 VGLWidget.ShaderVersion))
      except Exception as ex:
         print(f"Not implemented exception. {self.__class__} {__name__} :: {str(ex)}")


