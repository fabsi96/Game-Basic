
in vec2 passTextureCoord;

uniform sampler2D testTexture;

void main(void)
{
    gl_FragColor = texture(testTexture, passTextureCoord);
}