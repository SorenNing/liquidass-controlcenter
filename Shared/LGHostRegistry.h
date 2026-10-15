#pragma once

#include <stddef.h>
#include <string.h>

typedef struct {
    const char *identifier;
    const char *filterType;
    const char *preferencePrefix;
    float cornerRadiusRatio;
    float bezelWidthPoints;
    float glassThickness;
    float refractionScale;
    float refractiveIndex;
    float blur;
    float specularOpacity;
    float dispersionStrength;
    const char *lightTintHex;
    const char *darkTintHex;
} LGHostDefinition;

//    host            filter                            pref             corner          bezel      thick   refr  index  blur  spec   disp   light        dark
#define LG_HOST_REGISTRY(X) \
    X(Default,        "dylv.liquidglass.refraction",   "Default",         28.0f / 220.0f, 20.00f,    108.0f, 2.6f, 1.80f, 1.0f, 1.0f,  2.00f, "#FFFFFF1A", "#00000000") \
    X(ControlCenter,  "dylv.liquidglass.cc",           "ControlCenter",   28.0f / 220.0f, 15.50f,    120.0f, 1.8f, 1.60f, 0.0f, 1.0f,  2.00f, "#FFFFFF1A", "#00000000")

enum LGHostIdentifier {
#define LG_HOST_ENUM(identifier, ...) LGHostIdentifier##identifier,
    LG_HOST_REGISTRY(LG_HOST_ENUM)
#undef LG_HOST_ENUM
    LGHostIdentifierCount
};

static const LGHostDefinition kLGHostRegistry[LGHostIdentifierCount] = {
#define LG_HOST_ENTRY(identifier, filter, prefix, radius, bezel, thickness, refraction, index, blurValue, specular, dispersion, lightTint, darkTint) \
    { #identifier, filter, prefix, radius, bezel, thickness, refraction, index, blurValue, specular, dispersion, lightTint, darkTint },
    LG_HOST_REGISTRY(LG_HOST_ENTRY)
#undef LG_HOST_ENTRY
};

static inline enum LGHostIdentifier LGHostIdentifierForDefinition(const LGHostDefinition *host) {
    return host ? (enum LGHostIdentifier)(host - kLGHostRegistry) : LGHostIdentifierCount;
}

static inline const LGHostDefinition *LGHostDefinitionForPreferencePrefix(const char *prefix) {
    if (!prefix) return NULL;
    for (size_t i = 0; i < LGHostIdentifierCount; ++i)
        if (strcmp(kLGHostRegistry[i].preferencePrefix, prefix) == 0) return &kLGHostRegistry[i];
    return NULL;
}

static inline const LGHostDefinition *LGHostDefinitionForFilterType(const char *filterType) {
    if (!filterType) return NULL;
    for (size_t i = 0; i < LGHostIdentifierCount; ++i) {
        const char *base = kLGHostRegistry[i].filterType;
        size_t length = strlen(base);

        if (strncmp(filterType, base, length) == 0 &&
            (filterType[length] == '\0' || filterType[length] == '.')) return &kLGHostRegistry[i];
    }
    return NULL;
}

static inline enum LGHostIdentifier LGHostIdentifierForFilterType(const char *filterType) {
    return LGHostIdentifierForDefinition(LGHostDefinitionForFilterType(filterType));
}
