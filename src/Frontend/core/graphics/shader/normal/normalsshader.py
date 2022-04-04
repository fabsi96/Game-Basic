# encoding: utf-8

from core.graphics.shader.shaderloader import getShader
from core.graphics.shader.shaderprogram import ShaderProgram

# -----------------
from core.gui.vglwidget import VGLWidget


class NormalsShader(ShaderProgram):
    # -----------------
    """ Summary
    """

    # -----------------
    def __init__(self):
        # -----------------
        try:
            super(NormalsShader, self).__init__("normal",
                                                getShader("core/graphics/shader/normal", "normalsShader",
                                                          VGLWidget.ShaderVersion))
        except Exception as ex:
            print(f"Not implemented exception. {self.__class__} {__name__} :: {str(ex)}")
