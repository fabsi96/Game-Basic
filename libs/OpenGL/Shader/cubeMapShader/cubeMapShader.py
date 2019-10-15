# encoding: utf-8
from libs.OpenGL.Shader.shaderloader import getShader
from libs.OpenGL.Shader.shaderprogram import ShaderProgram
from libs.Qt.vwindow import VGLWindow


class CubeMapShader(ShaderProgram):
   def __init__(self):
      try:
         super(CubeMapShader, self).__init__("cubeMapShader", getShader("libs/OpenGL/Shader/cubeMapShader", "cubeMapShader", "cubeMapShader",VGLWindow.ShaderVersion))
      except Exception as ex:
         print(str(ex))