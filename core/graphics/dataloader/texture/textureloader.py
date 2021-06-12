# encoding: utf-8
import os
import numpy as np
from OpenGL.GL import *
from PIL import Image
from datetime import datetime

# ------------------------------------
def loadTexture(fullPath, COLOR_MODE) -> int:
    try:
        # texture
        texturevbo = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texturevbo)
        glEnable(GL_TEXTURE_2D)

        # Set the texture wrapping parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        # Set texture filtering parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        image = Image.open(fullPath)
        if COLOR_MODE == GL_RGB:
            image_rgb = image.convert("RGB")
            img_data = np.array(image_rgb.getdata())
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
        elif COLOR_MODE == GL_RGBA:
            image_rgba = image.convert("RGBA")
            img_data = np.array(image_rgba.getdata())
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

        return texturevbo

    except Exception as ex:
        raise ex
