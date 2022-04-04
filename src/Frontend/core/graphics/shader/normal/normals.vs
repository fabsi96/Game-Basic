
in vec3 vertexCoord;

uniform mat4 transformMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

void main(void)
{
    gl_Position = projectionMatrix * viewMatrix * transformMatrix * vec4(vertexCoord, 1.0);
    gl_PointSize = 10.0f;
}