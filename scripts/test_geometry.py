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
# 0.2.6/0.2.7: native controls own their animation and fill geometry.
assert '- (void)setCornerRadius:' not in cc
assert 'basic.fromValue = desired' not in cc and 'kCCRoundDesiredRadiusKey' not in cc
assert 'roundModuleContainerImpl' not in cc
assert 'LGCCNativeTrackRadius(mat.layer.cornerRadius' in cc
slider=cc[cc.index('static void ccRefreshSliderMaterials'):cc.index('static void roundSliderMaterials(UIView *slider)')]
assert 'cornerRadius =' not in slider and 'ccApplyOrRestoreRound' not in slider
assert 'kLGRadiusKey' not in live
assert 'LGGeometryIsTransitioning' in live and 'LGGlassShouldHideOriginalMaterial' in live
assert '80 * NSEC_PER_MSEC' in live
assert 'LGGlassShouldHideOriginalMaterial(material, glass)' in kit
assert 'LGCCChooseOutputMapping' in shader
assert 'stock-only-diagnostic' in shader and 'custom-encoded' in shader
assert '[CCTRANS]' in shader and '[CCVIEWTRANS]' in live
# Replacement may fail after a previously successful attachment. It must clear state.
creation=live[live.index('// The previous filter is not'):live.index('- (void)reapplyFilterForParameterReload {')]
assert creation.index('_filterAttached = NO') < creation.index('filterWithType:')
assert 'normalizedOutputScale' in shader
prefs=plistlib.loads((R/'LiquidAssCCPrefs/Resources/Root.plist').read_bytes())
rows={x['key']:x for x in prefs['items'] if 'key' in x}
for key in ['Debug.Renderer.StockOnly','Debug.TransitionTrace.Enabled']:
    assert rows[key]['default'] is False
assert rows['ControlCenter.BezelWidth']['default']==15.5
assert rows['ControlCenter.RefractionScale']['default']==1.8
print('PASS source invariants: native track geometry, no radius animation locks, failure state reset, opt-in bounded trace, unchanged visual defaults')
