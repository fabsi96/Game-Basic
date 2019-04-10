import os

from OpenGL.GL import *
import OpenGL.GL.shaders


def getShaderCode(dir_s, shader_file):
    shader_source = ""
    with open(os.path.join(dir_s, shader_file)) as f:
        shader_source = f.read()
    f.close()
    return shader_source

def getShader(dir_s, vs, fs, shaderVersion: int):
    vert_shader = "#version {}".format(str(shaderVersion)) + " \n " + getShaderCode(dir_s, vs + ".vs")
    frag_shader = "#version {}".format(str(shaderVersion)) + " \n " + getShaderCode(dir_s, fs + ".fs")

    shader = OpenGL.GL.shaders.compileProgram(OpenGL.GL.shaders.compileShader(vert_shader, GL_VERTEX_SHADER),
                                              OpenGL.GL.shaders.compileShader(frag_shader, GL_FRAGMENT_SHADER))
    return shader