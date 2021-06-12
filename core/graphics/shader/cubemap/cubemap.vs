
in vec3 vertexCoord;

out vec3 passTextureCoord;

uniform mat4 projectionMatrix;
uniform mat4 viewMatrix;

void main(void)
{
    mat4 mMatrix = viewMatrix;
    mMatrix[3][0] = 0;
    mMatrix[3][1] = 0;
    mMatrix[3][2] = 0;
    gl_Position = projectionMatrix * mMatrix * vec4(vertexCoord, 1.0);

    passTextureCoord = vertexCoord;
}