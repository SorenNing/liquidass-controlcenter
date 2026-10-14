#!/usr/bin/env python3
"""Compile extracted upstream sources to objects only. Never link or package."""
from pathlib import Path
import os, sys, subprocess, json, hashlib, time
ROOT = Path(__file__).resolve().parents[1]
THEOS = Path(os.environ.get('THEOS', '/var/minis/workspace/LiquidGlassCC/theos'))
SDK = Path(os.environ.get('IOS_SDK', str(THEOS / 'sdks/iPhoneOS16.5.sdk')))
OUT = ROOT / 'validation'
OUT.mkdir(exist_ok=True)
INCLUDE = OUT / 'include'
INCLUDE.mkdir(exist_ok=True)
# iSH cannot preserve the repository's symlinked substrate.h; use the real upstream header.
(INCLUDE / 'substrate.h').write_bytes((THEOS / 'vendor/lib/CydiaSubstrate.framework/Headers/CydiaSubstrate.h').read_bytes())
LOGOS = THEOS / 'vendor/logos/bin/logos.pl'
sources = ['Hooks/ControlCenter.x', 'Shared/LGGlassKit.x',
 'Shared/LGLiveBackdropView.m', 'Shared/LGSharedSupport.m', 'Shared/LGNativeBlurView.m',
 'LiquidAssBackboardd/Tweak.mm', 'LiquidAssBackboardd/LGSymbolResolver.mm', 'LiquidAssCCPrefs/LGCCRootListController.m']
records = []
for arch in ['arm64', 'arm64e']:
 directory = OUT / arch
 directory.mkdir(exist_ok=True)
 for name in sources:
  src = ROOT / name
  stem = name.replace('/', '_').replace('.', '_')
  if src.suffix == '.x':
   # Theos .x files are Objective-C, not Objective-C++. Match its ABI.
   generated = src.with_suffix('.validation.m')
   result = subprocess.run(['perl', str(LOGOS), '-c', 'generator=MobileSubstrate', str(src)], capture_output=True)
   (directory / (stem + '.logos.stderr')).write_bytes(result.stderr)
   if result.returncode:
    records.append(dict(arch=arch, source=name, stage='logos', exit=result.returncode))
    continue
   generated.write_bytes(result.stdout)
   use_src = generated
  else:
   use_src = src
  cmd = ['clang++' if use_src.suffix == '.mm' else 'clang', '-target', arch+'-apple-ios14.0',
   '-isysroot', str(SDK), '-fobjc-arc', '-fblocks', '-O1', '-fno-autolink',
   '-DTHEOS_PACKAGE_SCHEME_ROOTHIDE=1', '-DTHEOS_PACKAGE_INSTALL_PREFIX=""',
   '-I'+str(INCLUDE), '-I'+str(THEOS/'vendor/include'), '-I'+str(THEOS/'include'), '-I'+str(ROOT/'Shared')]
  if use_src.suffix == '.mm': cmd += ['-std=c++17', '-fno-objc-arc-exceptions']
  obj = directory/(stem+'.o')
  cmd += ['-c', str(use_src), '-o', str(obj)]
  start = time.monotonic()
  result = subprocess.run(cmd, capture_output=True)
  (directory/(stem+'.stderr')).write_bytes(result.stderr)
  (directory/(stem+'.stdout')).write_bytes(result.stdout)
  record = dict(arch=arch,source=name,stage='compile-object-only',exit=result.returncode,
   elapsed=round(time.monotonic()-start,2), command=cmd,
   source_sha256=hashlib.sha256(src.read_bytes()).hexdigest())
  records.append(record)
  print(arch, name, 'PASS' if result.returncode==0 else 'FAIL',flush=True)
  if src.suffix=='.x': generated.unlink(missing_ok=True)
  (OUT/'compile-report.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
print('Objects only. No dylib, DEB, signing, header rewriting, device injection or runtime tests.')
sys.exit(1 if any(r['exit'] for r in records) else 0)
