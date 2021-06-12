
in vec2 passTextureCoord;
in vec3 passNormalCoord;
in vec3 passTransformedVertexCoord;

// This part could be dynamic (from vmap class or shader class)
uniform sampler2D pathMapTexture;
uniform sampler2D pathTexture;
uniform sampler2D grassTexture;
uniform sampler2D sandTexture;

// Ambient light
uniform vec3 ambientLight;

// Point lights
// uniform int currentAmountLights;
const int MAX_LIGHTS = 10;
uniform vec3 pointLightsPosition[MAX_LIGHTS];

//uniform vec3 cameraPosition;

/*
 * Calculate texture color (without lights) from pathmap
 */
// ----------------------------------------
vec4 calcColorFromTexture(vec2 tiledCoords)
// ----------------------------------------
{
    vec4 pathMapColor = texture(pathMapTexture, passTextureCoord);

    /* => vec4().rgba */
    // Rot -/ Blau -/ Schwarz
    float blackAmount = 1 - (pathMapColor.r + pathMapColor.b + pathMapColor.g);
    vec4 grassColor = texture(grassTexture, tiledCoords) * blackAmount;
    vec4 pathColor = texture(pathTexture, tiledCoords) * pathMapColor.b;
    vec4 sandColor = texture(sandTexture, tiledCoords) * pathMapColor.r;

    return grassColor + pathColor + sandColor;
}

/* lightFaceVec -> Vector measured from vertex to light
 * Calculates factor of dividing light brightness
 */
// --------------------------------------------------------
float calcPointArea(vec3 lightFaceVector, vec3 attenuation)
// --------------------------------------------------------
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
    vec3 attenuation = vec3(.80f, .15f, .00f);;

    vec3 finalPointLight = vec3(0.0, 0.0, 0.0);
    // for (int i=0, i <= currentAmountLights; i++)
    for (int i=0; i <= MAX_LIGHTS; i++)
    {
        // TODO -> lightFaceVector (normalize())
        if (pointLights[i] == vec3(0.0))
            continue;
        vec3 lightFaceVector = pointLights[i] - passTransformedVertexCoord;
        float dotPointLight = dot(passNormalCoord, normalize(lightFaceVector));
        // float brightness = max(dotPointLight, 0.0);
        vec3 currentPointLight = (vec3(dotPointLight, dotPointLight, dotPointLight)) / calcPointArea(lightFaceVector, attenuation); // brightness * lightColor[i]
        finalPointLight += currentPointLight;
    }
    return finalPointLight;
}

// ------------
void main(void)
{
    // ------------
    // Ambient component
    vec4 ambientComponent = vec4(ambientLight, 1.0);

    // ------------
    // Point lights equasion
    vec4 pointLightComponent = vec4(calcPointLights(), 1.0);
    // pointLightComponent = max(pointLightComponent, 0.2);

    // ------------
    // Method for detailed texture visualization
    vec2 tiledCoords = passTextureCoord * 40.0;
    vec4 textureColor = calcColorFromTexture(tiledCoords);


    // ------------
    // Final color calculation
    gl_FragColor = (ambientComponent + pointLightComponent) * textureColor;
}