
in vec3 vertexCoord;
in vec2 textureCoord;
in vec3 normalCoord;

uniform mat4 transformMatrix;
uniform mat4 projectionMatrix;
uniform mat4 viewMatrix;

out vec2 passTextureCoord;
out vec3 passNormalCoord;
out vec3 passTransformedVertexCoord;

void main(void)
{
    gl_Position = projectionMatrix * viewMatrix * transformMatrix * vec4(vertexCoord, 1.0);

    passTextureCoord = textureCoord;
    passNormalCoord = normalCoord;
    passTransformedVertexCoord = vec3(transformMatrix * vec4(vertexCoord, 1.0));
}