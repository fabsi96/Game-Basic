# encoding: utf-8
from libs.OpenGL.Shader.shaderloader import getShader
from libs.OpenGL.Shader.shaderprogram import ShaderProgram
from libs.Qt.vwindow import VGLWindow


class MapShader (ShaderProgram):
   def __init__(self):
      super(MapShader, self).__init__("mapShader", getShader("libs/OpenGL/Shader/mapShader", "mapShader", "mapShader", VGLWindow.ShaderVersion))

