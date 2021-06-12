
in vec3 passTextureCoord;

uniform samplerCube cubeMap;

void main(void)
{
    gl_FragColor = texture(cubeMap, passTextureCoord);
}
