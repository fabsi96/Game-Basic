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
class CubeMapShader(ShaderProgram):
    """ Summary
    """
    CUBE_MAP_DIR = "CubeMapShader"

    """ Coordinates """
    VERTICES_NAME = "vertexCoord"

    """ Matrices """
    PROJECTION_MATRIX_NAME = "projectionMatrix"
    VIEW_MATRIX_NAME = "viewMatrix"

    # -----------------
    def __init__(self):
        try:
            super(CubeMapShader, self).__init__(self.CUBE_MAP_DIR,
                                                getShader(os.path.join(ShaderProgram.SHADER_DIR, self.CUBE_MAP_DIR),
                                                          self.CUBE_MAP_DIR,
                                                          VGLWidget.ShaderVersion))

            self.loadMatrix4x4(CubeMapShader.PROJECTION_MATRIX_NAME)
            self.loadMatrix4x4(CubeMapShader.VIEW_MATRIX_NAME)

        except Exception as ex:
            print(f"__init__: CubeMapShader [ERROR] {ex.args}")
            raise ex
