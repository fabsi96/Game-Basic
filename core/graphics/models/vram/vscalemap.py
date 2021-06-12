# encoding: utf-8
from core.graphics.models.ram.rawobject import RawObject
from core.graphics.models.vram.vopengl import VOpenGL
from core.graphics.shader.model.modelshader import ModelShader
from core.graphics.shader.shaderprogram import ShaderProgram


class VScaleMap(VOpenGL):
    def __init__(self, rawObject: RawObject, sp: ShaderProgram):
        try:
            super(VScaleMap, self).__init__(rawObject, sp)
            self._uploadTexture(rawObject.textureFiles[0], ModelShader.MODEL_TEXTURE_NAME, 0)

        except Exception as ex:
            print(f"__init__: VScaleMap [ERROR] {ex.args}")

    def render(self):
        super(VScaleMap, self).render()