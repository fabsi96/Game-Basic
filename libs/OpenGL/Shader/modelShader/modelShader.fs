in vec2 passTextureCoord;
in vec3 passTransformedNormalCoord;
in vec3 passTransformedVertexCoord;

uniform sampler2D testTexture;
uniform vec3 ambientLight;
uniform vec3 lightPosition;
uniform vec3 cameraPosition;


void main(void)
{
    // -- Diffuse light calculations in relation to vertex coord
    vec3 lightFaceVector = normalize(lightPosition - passTransformedVertexCoord);

    // -- Diffuse light calculation
    float dotProduct = dot(lightFaceVector, normalize(passTransformedNormalCoord));
    vec3 diffuseLight = vec3(dotProduct, dotProduct, dotProduct);

    // -- Specular light equation
    vec3 specularReflection = reflect(-lightFaceVector, passTransformedNormalCoord);
    vec3 worldCameraVector = normalize(cameraPosition - passTransformedVertexCoord);
    float specularity = dot(specularReflection, worldCameraVector);
    float s = pow(specularity, 80);
    vec4 specularLight = vec4(s, s, s, 1.0);

    gl_FragColor = (clamp(vec4(ambientLight, 1.0), 0, 1) + clamp(vec4(diffuseLight, 1.0), 0, 1)) * texture(testTexture, passTextureCoord);
}