
in vec3 vertexCoord;
in vec2 textureCoord;

uniform mat4 transformMatrix;
uniform mat4 projectionMatrix;
uniform mat4 viewMatrix;

out vec2 passTextureCoord;

void main(void)
{
    gl_Position = projectionMatrix * viewMatrix * transformMatrix * vec4(vertexCoord, 1.0);

    passTextureCoord = textureCoord;
}