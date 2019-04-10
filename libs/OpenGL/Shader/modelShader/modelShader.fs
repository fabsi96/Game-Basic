in vec2 passTextureCoord;
in vec3 passNormalCoord;
in vec3 lightFaceVector;

uniform sampler2D testTexture;
uniform vec3 lightColor;

void main(void)
{
    vec3 modelNormal = normalize(passNormalCoord);
    vec3 modelLightFaceVector = normalize(lightFaceVector);

    // Calculation
    float dotProd = dot(modelNormal, modelLightFaceVector);
    float brightness = max(dotProd, 0.0);
    vec3 diffuseLight = brightness * lightColor;

    gl_FragColor = vec4(diffuseLight, 1.0) * texture(testTexture, passTextureCoord);
    // discard; ->
}