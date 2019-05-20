# encoding: utf-8
from libs.OpenGL.Shader.shaderloader import getShader
from libs.OpenGL.Shader.shaderprogram import ShaderProgram
from libs.Qt.vwindow import VWindow, VGLWindow


class NormalsShader(ShaderProgram):
   def __init__(self):
      super(NormalsShader, self).__init__("NormalsShader", getShader("libs/OpenGL/Shader/NormalsShader", "normalsShader", "normalsShader", VGLWindow.ShaderVersion))

