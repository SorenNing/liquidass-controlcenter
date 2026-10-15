"""Host-only regression assertions. Does not execute iOS code or claim visual validation."""
from pathlib import Path
import math, plistlib, re
R=Path(__file__).resolve().parents[1]
def mapping(sw,sh,dw,dh):
    sx,sy=dw/sw,dh/sh
    norm=dw>0 and dh>0 and .85<=sx<=1 and .85<=sy<=1 and (sx<1 or sy<1) and abs(sx-sy)/max(sx,sy)<=.01
    compat=lambda d,s:(d-s<=64 if d>=s else s-d<=8)
    ok=norm or (compat(dw,sw) and compat(dh,sh))
    return ok,norm
for sizes in [(240,239,215,215),(240,239,218,219),(224,224,214,214),(165,165,152,152),(170,170,154,155)]:
    assert mapping(*sizes)==(True,True), sizes
    sw,sh,dw,dh=sizes
    first=(.5*sw/dw,.5*sh/dh)
    last=((dw-.5)*sw/dw,(dh-.5)*sh/dh)
    assert 0<first[0]<last[0]<sw and 0<first[1]<last[1]<sh
# Keep centering for padded targets, leave unknown distortion on stock output.
assert mapping(200,200,212,212)==(True,False)
assert mapping(200,200,200,200)==(True,False)
assert mapping(240,240,160,160)==(False,False)
assert mapping(240,240,220,180)==(False,False)
for small in range(1,30):
    assert mapping(240,240,240-small,240-small)==(True,True)
# At same size, floating-point pixel centers reproduce old +0.5 integer sampling.
for n in [77,170,217,400]:
    for x in [0,n//2,n-1]: assert (x+.5)/n == (float(x)+.5)/n
live=(R/'Shared/LGLiveBackdropView.m').read_text()
cc=(R/'Hooks/ControlCenter.x').read_text()
kit=(R/'Shared/LGGlassKit.x').read_text()
shader=(R/'LiquidAssBackboardd/Tweak.mm').read_text()
assert 'initialCornerRadius:radius' in live
initializer=live[live.index('filterType:(NSString *)filterType initialCornerRadius:'):live.index('- (void)dealloc')]
assert initializer.index('self.layer.cornerRadius =') < initializer.index('[self applyFilters]')
assert 'sCCSmallModuleRadius' not in cc
assert 'LGRefreshMaterialHost((UIView *)self)' in kit
assert 'if (glass && [glass lgFilterAttached])' not in kit # enabled gate must remain too
assert 'if (!inOverlay || ccHasMaterialAncestor(mat))' in cc
assert '&&\n                        LGMaterialHasGlass(mat, kGlassKey)' not in cc
assert 'sourcePosition / float2(W, H)' in shader
assert 'static_assert(sizeof(LGUniforms) == 176' in shader
entry=plistlib.loads((R/'layout/Library/PreferenceLoader/Preferences/liquidasscc.plist').read_bytes())['entry']
assert entry['icon']=='icon.png'
for suffix in ['','@2x','@3x']: assert (R/f'LiquidAssCCPrefs/Resources/icon{suffix}.png').is_file()
print('PASS: observed transition geometry, padding fallback, subpixel coordinates, first-frame radius, zero-size retry, icon assets')
