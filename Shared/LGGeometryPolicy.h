#pragma once
#include <math.h>
#include <stdint.h>

// Negative means "not ready": retain stock material instead of inventing a radius.
static inline double LGCCNativeTrackRadius(double nativeRadius, double width, double height) {
    if (!isfinite(nativeRadius) || !isfinite(width) || !isfinite(height) ||
        nativeRadius <= 0.0 || width <= 0.0 || height <= 0.0) return -1.0;
    return fmin(nativeRadius, fmin(width, height) * 0.5);
}

enum LGCCOutputMapping {
    LGCCOutputStock = 0,
    LGCCOutputCentered = 1,
    LGCCOutputNormalized = 2,
};

static inline int LGCCCenteredDimension(uint64_t destination, uint64_t source) {
    return destination >= source ? destination - source <= 64 : source - destination <= 8;
}

// The 0.2.5 limits are deliberately retained, not relaxed to hide stock fallbacks.
static inline enum LGCCOutputMapping LGCCChooseOutputMapping(uint64_t sw, uint64_t sh,
                                                            uint64_t dw, uint64_t dh,
                                                            int isControlCenter) {
    if (!sw || !sh || !dw || !dh) return LGCCOutputStock;
    double sx = (double)dw / sw, sy = (double)dh / sh;
    if (isControlCenter && sx >= 0.85 && sy >= 0.85 && sx <= 1.0 && sy <= 1.0 &&
        (sx < 1.0 || sy < 1.0) && fabs(sx - sy) / fmax(sx, sy) <= 0.01)
        return LGCCOutputNormalized;
    if (LGCCCenteredDimension(dw, sw) && LGCCCenteredDimension(dh, sh))
        return LGCCOutputCentered;
    return LGCCOutputStock;
}
