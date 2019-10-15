// ** Object information
in vec3 vertexCoord;
in vec2 textureCoord;
in vec3 normalCoord;

// -- Vertex transform for 3d
uniform mat4 transformMatrix;
uniform mat4 projectionMatrix;
uniform mat4 viewMatrix;


out vec2 passTextureCoord;
out vec3 passNormalCoord;
out vec3 passTransformedVertexCoord;


void main(void)
{
    // -- Calculate right position on screen
    vec4 modelTransformation = transformMatrix * vec4(vertexCoord, 1.0);
    gl_Position = projectionMatrix * viewMatrix * modelTransformation;

    // -- Passing texture coords for further processing in fragment shader
    passTextureCoord = textureCoord;
    passNormalCoord = normalCoord;
    passTransformedVertexCoord = modelTransformation.xyz;
}