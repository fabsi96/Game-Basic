
in vec2 passTextureCoord;
in vec3 passTransformedNormalCoord;
in vec3 passTransformedVertexCoord;

uniform sampler2D modelTexture;
// Ambient color
uniform vec3 ambientLight;

// Array of point lights
// uniform int currentAmountLights;
const int MAX_LIGHTS = 10;
uniform vec3 pointLightsPosition[MAX_LIGHTS];
uniform vec3 pointLightsAttenuation[MAX_LIGHTS];

// Camera position for specularity
uniform vec3 cameraPosition;

/*
 * lightFaceVec -> Vector measured from vertex to light
 * Calculates factor of dividing light brightness
 */
// --------------------------------------------------------
float calcPointArea(vec3 lightFaceVector, vec3 attenuation)
{
    float lengthToLight = length(lightFaceVector);
    return attenuation.x + attenuation.y * lengthToLight + attenuation.z * pow(lengthToLight, 2);
}

/*
 * Sums up point lights from diffrent positions (locations)
 *
 */
// -------------------
vec3 calcPointLights()
{
    // Diffuse light calculations in relation to vertex coord
    vec3 finalPointLight = vec3(0.0, 0.0, 0.0);
    // for (int i=0, i <= currentAmountLights; i++)
    for (int i=0; i <= MAX_LIGHTS; i++)
    {
        vec3 currentPointLightPosition = pointLightsPosition[i];
        vec3 currentPointLightAttenuation = pointLightsAttenuation[i];
        if (currentPointLightPosition == vec3(0.0) ||
            currentPointLightAttenuation == vec3(0.0))
            continue;

        vec3 lightFaceVector = currentPointLightPosition - passTransformedVertexCoord;
        float dotPointLight = dot(normalize(lightFaceVector), passTransformedNormalCoord);
        vec3 currentPointLight = vec3(dotPointLight, dotPointLight, dotPointLight) / calcPointArea(lightFaceVector, currentPointLightAttenuation);
        finalPointLight += currentPointLight;
    }

    return finalPointLight;
}

// -----------
void main(void)
{
    // -----------
    // Ambient color
    vec4 ambientComponent = vec4(ambientLight, 1.0);

    // -----------
    // Diffuse light component
    vec4 pointLightComponent = vec4(calcPointLights(), 1.0);

    // -----------
    // Specular light equation
    vec3 lightFaceVector = vec3(0.0, 0.0, 0.0);
    vec3 specularReflection = reflect(-lightFaceVector, passTransformedNormalCoord);
    vec3 worldCameraVector = normalize(cameraPosition - passTransformedVertexCoord);
    float specularity = dot(specularReflection, worldCameraVector);
    float s = pow(specularity, 80);
    vec4 specularLight = vec4(s, s, s, 1.0);

    // -----------
    // Final color calculation
    gl_FragColor = (ambientComponent + pointLightComponent) *  texture(modelTexture, passTextureCoord);
}