import os

from OpenGL.GL import *
import OpenGL.GL.shaders

# ------------------------------------
def getShaderCode(dir_s: str, shader_file: str) -> str:
# ------------------------------------
    with open(os.path.join(dir_s, shader_file)) as f:
        shader_source = f.read()
    f.close()
    return shader_source

# ---------------------------------------------------------------------
def getShader(dir_s: str, name_s: str, shaderVersion: int) -> int:
    try:
        baseShaderName = name_s[0].lower() + name_s[1:len(name_s)]
        vert_shader = "#version {}".format(str(shaderVersion)) + " \n " + getShaderCode(dir_s, baseShaderName + ".vs")
        frag_shader = "#version {}".format(str(shaderVersion)) + " \n " + getShaderCode(dir_s, baseShaderName + ".fs")
        shader = OpenGL.GL.shaders.compileProgram(OpenGL.GL.shaders.compileShader(vert_shader, GL_VERTEX_SHADER),
                                                  OpenGL.GL.shaders.compileShader(frag_shader, GL_FRAGMENT_SHADER))
        return shader
    except Exception as ex:
        raise ex