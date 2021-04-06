# encoding: utf-8
from libs.Qt.vglwidget import VGLWidget

try:
    import os
    from OpenGL.GL import *
    import numpy as np1

except Exception as e:
    print(f"Import exception {str(e)}")

try:
    from libs.OpenGL.Shader.shaderloader import getShader
    from libs.OpenGL.Shader.shaderprogram import ShaderProgram
except Exception as e:
    print(f"Import exception {str(e)}")


# -----------------
class ModelShader(ShaderProgram):
    """ Summary
    """
    MODEL_DIR = "ModelShader"

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
            print(f"[ERROR] ModelShader - __init__() :: {str(ex)}")
