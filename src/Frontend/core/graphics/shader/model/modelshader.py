# encoding: utf-8
from core.gui.vglwidget import VGLWidget

try:
    import os
    from OpenGL.GL import *
    import numpy as np1

except Exception as e:
    print(f"Import exception {str(e)}")

try:
    from core.graphics.shader.shaderloader import getShader
    from core.graphics.shader.shaderprogram import ShaderProgram
except Exception as e:
    print(f"Import exception {str(e)}")


# -----------------
class ModelShader(ShaderProgram):
    """ Summary
    """
    MODEL_DIR = "model"

    """ Vectors """
    VERTICES_NAME = "vertexCoord"
    TEXTURES_NAME = "textureCoord"
    NORMALS_NAME = "normalCoord"

    """ Textures """
    MODEL_TEXTURE_NAME = "modelTexture"

    """ Matrices """
    TRANSFORMATION_MATRIX_NAME = "transformMatrix"
    PROJECTION_MATRIX_NAME = "projectionMatrix"
    VIEW_MATRIX_NAME = "viewMatrix"

    # -----------------
    def __init__(self):
        try:
            super(ModelShader, self).__init__(self.MODEL_DIR,
                                              getShader(os.path.join(ShaderProgram.SHADER_DIR,
                                                                     self.MODEL_DIR),
                                                        self.MODEL_DIR,
                                                        VGLWidget.ShaderVersion))
            self.loadMatrix4x4(ModelShader.TRANSFORMATION_MATRIX_NAME)
            self.loadMatrix4x4(ModelShader.PROJECTION_MATRIX_NAME)
            self.loadMatrix4x4(ModelShader.VIEW_MATRIX_NAME)

        except Exception as ex:
            print(f"[ERROR] model - __init__() :: {str(ex)}")
