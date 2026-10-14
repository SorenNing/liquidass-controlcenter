#!/usr/bin/env python3
"""Isolate only prefs, IPC and state strings; do not touch shader/filter names."""
from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
repls={
 'liquidass-backboardd':'liquidasscc-backboardd',
 'liquidass-gaussian-identity':'liquidasscc-gaussian-identity',
 'liquidass-safemode.log':'liquidasscc-safemode.log',
 'liquidglass.log':'liquidasscc.log',
 'dylv.liquidass/BackboarddSafeMode':'com.minis.liquidasscc/BackboarddSafeMode',
 'dylv.liquidglass/ParametersReloaded':'com.minis.liquidasscc/ParametersReloaded',
}
files=['Shared/LGSharedSupport.m','Shared/LGLiveBackdropView.m','Shared/LGGlassKit.x',
 'LiquidAssBackboardd/Tweak.mm','LiquidAssBackboardd/LGSymbolResolver.mm']
report=[]
for name in files:
 p=root/name; old=p.read_text(); s=old; counts={}
 for a,b in repls.items():
  n=s.count(a)
  if n: counts[a]=n; s=s.replace(a,b)
 if s!=old: p.write_text(s)
 report.append({'file':name,'replacements':counts})
(root/'validation/isolation-edits.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
