# encoding: utf-8
from libs.OpenGL.DAL.Inner.rawobject import RawObject
from libs.OpenGL.DAL.Outer.vopengl import VOpenGL
from libs.OpenGL.Shader.ModelShader.modelshader import ModelShader

from libs.OpenGL.Shader.shaderprogram import ShaderProgram
from glm import *

# --------------------------------
class VLightSource(VOpenGL):
    """ Summary
       This class represents a light source
       * Updates every shader for correct light calculations
       * The exact light source could be inside of a VObject (Cube, Sphere)
       * This class could inherit multiple object-parts
    """

    # --------------------------------
    def __init__(self, rawObject: RawObject, sp: ShaderProgram):
        try:
            super(VLightSource, self).__init__(rawObject, sp)
            self._xAttenuation = 1.0
            self._yAttenuation = 1.0
            self._zAttenuation = 1.0
            self._attenuation = vec3(1.0, 1.0, 1.0)

            self._uploadTexture(rawObject.textureFiles[0], ModelShader.MODEL_TEXTURE_NAME, 0)
            ShaderProgram.addLightSource(self)

        except Exception as ex:
            print(f"__init__: VLightSource [ERROR] {ex.args}")

    # --------------------------------
    def setAttenuation(self, attenuation: vec3) -> None:
        self._attenuation = attenuation
        self.sp.updateLightSources()

    # --------------------------------
    def getAttenuation(self) -> vec3:
        return self._attenuation

    # --------------------------------
    def setPosition(self, newPos: vec3) -> None:
        super(VLightSource, self).setPosition(newPos)

    def render(self):
        super(VLightSource, self).render()
        self.sp.updateLightSources()
