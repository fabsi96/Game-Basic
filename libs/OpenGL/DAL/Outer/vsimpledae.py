# encoding: utf-8
from libs.OpenGL.DAL.Inner.rawobject import RawObject
from libs.OpenGL.DAL.Outer.vopengl import VOpenGL
from libs.OpenGL.Shader.ModelShader.modelshader import ModelShader

from OpenGL.GL import *

from libs.library import Library


# -------------------------
class VSimpleDae(VOpenGL):

    # -------------------------
    def __init__(self, daeName: str, rawDae: RawObject, daeTexture):
        super(VSimpleDae, self).__init__(daeName, ModelShader(), VOpenGL.RENDER_ARRAYS)
        self.name = daeName

        self.vao = glGenVertexArrays(1)
        self.vertexVbo = self.uploadVertexData(self.vao,
                                               rawDae.vertexCoords,
                                               self.sp, ModelShader.VERTICES_NAME,
                                               3)
        self.vertexCount = len(rawDae.vertexCoords)
        self.textureVbo = self.uploadVertexData(self.vao,
                                                rawDae.textureCoords,
                                                self.sp,
                                                ModelShader.TEXTURES_NAME,
                                                2)
        self.normalVbo = self.uploadVertexData(self.vao,
                                               rawDae.normalCoords,
                                               self.sp,
                                               ModelShader.NORMALS_NAME,
                                               3)

        del rawDae

        self._uploadTexture(daeTexture,
                            ModelShader.MODEL_TEXTURE_NAME,
                            0)

    # -------------------------
    def render(self):
        try:

            self.sp.start()
            self.sp.setMatrix4x4(ModelShader.TRANSFORMATION_MATRIX_NAME,
                                 self.getTransformationMatrix())
            self.sp.setMatrix4x4(ModelShader.PROJECTION_MATRIX_NAME,
                                 Library.mainWindow.getProjectionMatrix())
            self.sp.setMatrix4x4(ModelShader.VIEW_MATRIX_NAME,
                                 Library.camera.getWorldToViewMatrix())

            glBindVertexArray(self.vao)
            if self.renderMode == VOpenGL.RENDER_ARRAYS:
                glBindBuffer(GL_ARRAY_BUFFER, self.vertexVbo)
                for texture in self.textures:
                    glActiveTexture(GL_TEXTURE0 + texture.unit)
                    glBindTexture(GL_TEXTURE_2D, texture.vbo)
                    glDrawArrays(GL_TRIANGLES, 0, self.vertexCount)

            glBindVertexArray(0)
            self.sp.stop()

        except Exception as ex:
            print(f"render: VSimpleDae [ERROR] {ex.args}")