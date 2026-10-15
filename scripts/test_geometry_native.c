#include "../Shared/LGGeometryPolicy.h"
#include <assert.h>
#include <stdio.h>
int main(void) {
    assert(LGCCNativeTrackRadius(21,77,170)==21);
    assert(LGCCNativeTrackRadius(42,150,400)==42);
    assert(LGCCNativeTrackRadius(75,150,400)==75);
    assert(LGCCNativeTrackRadius(50,77,170)==38.5);
    assert(LGCCNativeTrackRadius(0,150,400)<0);
    assert(LGCCNativeTrackRadius(NAN,150,400)<0);
    assert(LGCCNativeTrackRadius(42,0,0)<0);
    assert(LGCCChooseOutputMapping(240,239,217,216,1)==LGCCOutputNormalized);
    assert(LGCCChooseOutputMapping(217,216,217,216,1)==LGCCOutputCentered);
    assert(LGCCChooseOutputMapping(200,200,212,212,1)==LGCCOutputCentered);
    assert(LGCCChooseOutputMapping(240,239,217,216,0)==LGCCOutputStock);
    // New device log fallbacks must remain fail-closed, not get silently widened.
    assert(LGCCChooseOutputMapping(231,510,202,472,1)==LGCCOutputStock);
    assert(LGCCChooseOutputMapping(340,155,306,138,1)==LGCCOutputStock);
    assert(LGCCChooseOutputMapping(402,157,383,174,1)==LGCCOutputStock);
    assert(LGCCChooseOutputMapping(147,146,138,139,1)==LGCCOutputStock);
    assert(LGCCChooseOutputMapping(165,165,154,156,1)==LGCCOutputStock);
    assert(LGCCChooseOutputMapping(197,458,183,415,1)==LGCCOutputStock);
    assert(LGCCChooseOutputMapping(183,415,179,399,1)==LGCCOutputStock);
    assert(LGCCChooseOutputMapping(155,155,140,138,1)==LGCCOutputStock);
    assert(LGCCChooseOutputMapping(200,200,0,200,1)==LGCCOutputStock);
    puts("PASS native policy: 21/42pt track radii, zero/NaN rejection, unchanged 0.2.5 mapping guards");
    return 0;
}
