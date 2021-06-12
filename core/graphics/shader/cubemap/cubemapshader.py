# encoding: utf-8
import os
from core.graphics.shader.shaderloader import getShader
from core.graphics.shader.shaderprogram import ShaderProgram
from core.gui.vglwidget import VGLWidget


class CubeMapShader(ShaderProgram):
    """ Summary
    """
    CUBE_MAP_DIR = "cubemap"

    """ Coordinates """
    VERTICES_NAME = "vertexCoord"

    """ Matrices """
    PROJECTION_MATRIX_NAME = "projectionMatrix"
    VIEW_MATRIX_NAME = "viewMatrix"

    def __init__(self):
        try:
            super(CubeMapShader, self).__init__(self.CUBE_MAP_DIR,
                                                getShader(os.path.join(ShaderProgram.SHADER_DIR, self.CUBE_MAP_DIR),
                                                          self.CUBE_MAP_DIR,
                                                          VGLWidget.ShaderVersion))

            self.loadMatrix4x4(CubeMapShader.PROJECTION_MATRIX_NAME)
            self.loadMatrix4x4(CubeMapShader.VIEW_MATRIX_NAME)

        except Exception as ex:
            print(f"__init__: cubemap [ERROR] {ex.args}")
            raise ex
