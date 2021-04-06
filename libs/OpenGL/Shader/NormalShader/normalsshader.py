# encoding: utf-8

from libs.OpenGL.Shader.shaderloader import getShader
from libs.OpenGL.Shader.shaderprogram import ShaderProgram

# -----------------
from libs.Qt.vglwidget import VGLWidget


class NormalsShader(ShaderProgram):
    # -----------------
    """ Summary
    """

    # -----------------
    def __init__(self):
        # -----------------
        try:
            super(NormalsShader, self).__init__("NormalShader",
                                                getShader("libs/OpenGL/Shader/NormalShader", "normalsShader",
                                                          VGLWidget.ShaderVersion))
        except Exception as ex:
            print(f"Not implemented exception. {self.__class__} {__name__} :: {str(ex)}")
