# encoding: utf-8
from libs.OpenGL.DAL.Inner.rawobject import RawObject
from libs.OpenGL.DAL.Outer.vopengl import VOpenGL
from libs.OpenGL.Shader.ModelShader.modelshader import ModelShader
from libs.OpenGL.Shader.shaderprogram import ShaderProgram


class VScaleMap(VOpenGL):
    def __init__(self, rawObject: RawObject, sp: ShaderProgram):
        try:
            super(VScaleMap, self).__init__(rawObject, sp)
            self._uploadTexture(rawObject.textureFiles[0], ModelShader.MODEL_TEXTURE_NAME, 0)

        except Exception as ex:
            print(f"__init__: VScaleMap [ERROR] {ex.args}")

    def render(self):
        super(VScaleMap, self).render()