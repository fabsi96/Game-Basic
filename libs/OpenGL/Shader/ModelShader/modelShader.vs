// ** Object information
in vec3 vertexCoord;
in vec2 textureCoord;
in vec3 normalCoord;

// -- Vertex transform for 3d
uniform mat4 transformMatrix;
uniform mat4 projectionMatrix;
uniform mat4 viewMatrix;


out vec2 passTextureCoord;
out vec3 passTransformedNormalCoord;
out vec3 passTransformedVertexCoord;


// -----------
void main(void)
{
    // -- Calculate right position on screen
    vec4 modelTransformation = transformMatrix * vec4(vertexCoord, 1.0);
    gl_Position = projectionMatrix * viewMatrix * modelTransformation;

    // -- Passing texture coords for further processing in fragment shader
    passTextureCoord = textureCoord;
    passTransformedNormalCoord = (transformMatrix * vec4(normalCoord, 0.0)).xyz;
    passTransformedVertexCoord = modelTransformation.xyz;
}