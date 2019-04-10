in vec3 vertexCoord;
in vec2 textureCoord;
// --
in vec3 normalCoord;

uniform mat4 transformMatrix;
uniform mat4 projectionMatrix;
uniform mat4 viewMatrix;
// --
uniform vec3 lightPosition;

out vec2 passTextureCoord;
// --
out vec3 passNormalCoord;
out vec3 lightFaceVector;

void main(void)
{
    passTextureCoord = textureCoord;

    passNormalCoord = vec3(transformMatrix * vec4(normalCoord, 0.0)).xyz;
    lightFaceVector = lightPosition - vertexCoord;

    gl_Position = projectionMatrix * viewMatrix * transformMatrix * vec4(vertexCoord, 1.0);
}